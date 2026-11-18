"""Agent MT5 temps réel : scanne le marché forex, classe les opportunités, gère le risque.
Nécessite Windows + terminal MT5 ouvert + `pip install MetaTrader5 pandas`."""
import time, datetime as dt
import pandas as pd
import MetaTrader5 as mt5
import config as C
from strategy import score
from telegram_bot import Telegram

STATE = {"running": True, "live": C.LIVE_TRADING, "quit": False}
TG = None

TF = {"M5": mt5.TIMEFRAME_M5, "M15": mt5.TIMEFRAME_M15, "H1": mt5.TIMEFRAME_H1, "H4": mt5.TIMEFRAME_H4}

def bars(sym, tf, n=300):
    r = mt5.copy_rates_from_pos(sym, TF[tf], 0, n)
    return None if r is None or len(r) < 210 else pd.DataFrame(r)

def lot_size(sym, sl_dist):
    info, acc = mt5.symbol_info(sym), mt5.account_info()
    risk = acc.equity * C.RISK_PER_TRADE
    per_lot = sl_dist / info.trade_tick_size * info.trade_tick_value
    lots = max(info.volume_min, min(info.volume_max, risk / per_lot))
    return round(round(lots / info.volume_step) * info.volume_step, 2)

def daily_pnl_ok():
    start = dt.datetime.now().replace(hour=0, minute=0, second=0)
    deals = mt5.history_deals_get(start, dt.datetime.now()) or []
    pnl = sum(d.profit for d in deals) + sum(p.profit for p in (mt5.positions_get() or []))
    return pnl > -C.DAILY_LOSS_LIMIT * mt5.account_info().balance

def place(sym, direction, a):
    tick = mt5.symbol_info_tick(sym)
    price = tick.ask if direction == "BUY" else tick.bid
    sgn = 1 if direction == "BUY" else -1
    sl, tp = price - sgn * C.SL_ATR * a, price + sgn * C.TP_ATR * a
    req = dict(action=mt5.TRADE_ACTION_DEAL, symbol=sym, volume=lot_size(sym, C.SL_ATR * a),
               type=mt5.ORDER_TYPE_BUY if direction == "BUY" else mt5.ORDER_TYPE_SELL,
               price=price, sl=sl, tp=tp, deviation=10, magic=C.MAGIC, comment="mt5_agent",
               type_time=mt5.ORDER_TIME_GTC, type_filling=mt5.ORDER_FILLING_IOC)
    res = mt5.order_send(req)
    ok = res and res.retcode == mt5.TRADE_RETCODE_DONE
    msg = f"{'✅' if ok else '❌'} {direction} {sym} {req['volume']} lots @ {price:.5f} SL {sl:.5f} TP {tp:.5f}" + ("" if ok else f" ({res})")
    print("  ->", msg); TG.send(msg)

def scan():
    opps = []
    for sym in C.SYMBOLS:
        if not mt5.symbol_select(sym, True): continue
        e, t = bars(sym, C.TF_ENTRY), bars(sym, C.TF_TREND)
        if e is None or t is None: continue
        direction, pts, a, why = score(e, t)
        info = mt5.symbol_info(sym)
        if info.spread * info.point > C.MAX_SPREAD_ATR * a: continue  # spread trop large
        opps.append((pts, sym, direction, a, why))
    return sorted(opps, reverse=True)

def status():
    acc = mt5.account_info()
    pos = [p for p in (mt5.positions_get() or []) if p.magic == C.MAGIC]
    lines = [f"{'▶️ actif' if STATE['running'] else '⏸ pause'} | {'RÉEL' if STATE['live'] else 'signaux'}",
             f"Solde {acc.balance:.2f} | Équité {acc.equity:.2f} {acc.currency}"]
    lines += [f"• {p.symbol} {'BUY' if p.type == 0 else 'SELL'} {p.volume} : {p.profit:+.2f}" for p in pos] or ["Aucune position"]
    return "\n".join(lines)

def main():
    global TG
    for attempt in range(5):
        ok = mt5.initialize(path=C.MT5_PATH, timeout=60000) if C.MT5_PATH else mt5.initialize(timeout=60000)
        if ok: break
        print(f"MT5 init échouée ({attempt + 1}/5): {mt5.last_error()} — nouvel essai dans 5 s"); time.sleep(5)
    else:
        raise SystemExit("Impossible de joindre MT5 : ouvrez le terminal, connectez le compte, "
                         "et lancez PowerShell SANS mode administrateur (ou renseignez MT5_PATH dans config.py).")
    TG = Telegram(STATE, status); TG.start()
    print(f"Connecté: {mt5.account_info().login} | LIVE={STATE['live']}")
    TG.send("🤖 Agent MT5 en ligne\n" + status())
    alerted = {}
    try:
        while not STATE["quit"]:
            if not STATE["running"]: time.sleep(2); continue
            print(f"\n[{dt.datetime.now():%H:%M:%S}] Scan")
            mine = [p for p in (mt5.positions_get() or []) if p.magic == C.MAGIC]
            for pts, sym, d, a, why in scan():
                flag = "★" if pts >= C.MIN_SCORE else " "
                print(f"{flag} {sym:7} {d:4} score={pts:3}  {', '.join(why)}")
                if pts < C.MIN_SCORE: continue
                if time.time() - alerted.get((sym, d), 0) > 3600:  # 1 alerte/h par signal
                    alerted[(sym, d)] = time.time(); TG.send(f"★ {sym} {d} score {pts}\n" + ", ".join(why))
                if (STATE["live"] and len(mine) < C.MAX_OPEN_POSITIONS
                        and sym not in {p.symbol for p in mine} and daily_pnl_ok()):
                    place(sym, d, a); mine = [p for p in (mt5.positions_get() or []) if p.magic == C.MAGIC]
            for _ in range(C.SCAN_INTERVAL_SEC):
                if STATE["quit"]: break
                time.sleep(1)
    finally:
        TG.send("⏹ Agent arrêté"); mt5.shutdown()

if __name__ == "__main__":
    main()
