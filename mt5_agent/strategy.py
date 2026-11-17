"""Score d'opportunité multi-timeframe : tendance H1 + pullback/momentum M15."""
from indicators import ema, rsi, atr, adx

def score(entry, trend):
    """entry/trend: DataFrames OHLC. Retourne (direction, score 0-100, atr, raisons)."""
    t_fast, t_slow = ema(trend.close, 50).iloc[-1], ema(trend.close, 200).iloc[-1]
    direction = "BUY" if t_fast > t_slow else "SELL"
    sgn = 1 if direction == "BUY" else -1
    c = entry.close
    e20, e50 = ema(c, 20), ema(c, 50)
    r, a, x = rsi(c).iloc[-1], atr(entry).iloc[-1], adx(entry).iloc[-1]
    pts, why = 0, []
    if sgn * (e20.iloc[-1] - e50.iloc[-1]) > 0: pts += 25; why.append("EMA20/50 alignées")
    if x > 25: pts += 20; why.append(f"ADX {x:.0f}")
    if (direction == "BUY" and 40 <= r <= 60) or (direction == "SELL" and 40 <= r <= 60): pts += 15; why.append(f"RSI neutre {r:.0f}")
    dist = abs(c.iloc[-1] - e20.iloc[-1]) / a
    if dist < 0.5: pts += 20; why.append("pullback sur EMA20")
    last = entry.iloc[-1]
    if sgn * (last.close - last.open) > 0 and abs(last.close - last.open) > 0.3 * a: pts += 20; why.append("bougie de reprise")
    return direction, pts, a, why
