"""Pilotage de l'agent par Telegram (long polling, sans dépendance externe hormis requests)."""
import threading, time, requests
import config as C

class Telegram:
    def __init__(self, state, status_fn):
        self.state, self.status_fn, self.offset = state, status_fn, 0
        self.url = f"https://api.telegram.org/bot{C.TELEGRAM_TOKEN}"
        self.enabled = bool(C.TELEGRAM_TOKEN and C.TELEGRAM_CHAT_ID)

    def send(self, text):
        if not self.enabled: return
        try: requests.post(f"{self.url}/sendMessage", data={"chat_id": C.TELEGRAM_CHAT_ID, "text": text}, timeout=10)
        except requests.RequestException as e: print("Telegram:", e)

    def handle(self, cmd):
        s = self.state
        if cmd == "/start": s["running"] = True; return "▶️ Agent démarré"
        if cmd == "/stop": s["running"] = False; return "⏸ Agent en pause"
        if cmd == "/live on": s["live"] = True; return "⚠️ Trading RÉEL activé"
        if cmd == "/live off": s["live"] = False; return "🛡 Mode signaux seulement"
        if cmd == "/status": return self.status_fn()
        if cmd == "/quit": s["quit"] = True; return "⏹ Arrêt complet de l'agent"
        return "Commandes : /start /stop /live on /live off /status /quit"

    def _loop(self):
        while not self.state["quit"]:
            try:
                r = requests.get(f"{self.url}/getUpdates", params={"offset": self.offset, "timeout": 30}, timeout=40).json()
                for u in r.get("result", []):
                    self.offset = u["update_id"] + 1
                    m = u.get("message") or {}
                    if str(m.get("chat", {}).get("id")) != str(C.TELEGRAM_CHAT_ID): continue  # ignore les inconnus
                    self.send(self.handle((m.get("text") or "").strip().lower()))
            except Exception as e:
                print("Telegram:", e); time.sleep(5)

    def start(self):
        if self.enabled: threading.Thread(target=self._loop, daemon=True).start()
        else: print("Telegram désactivé (TELEGRAM_TOKEN / TELEGRAM_CHAT_ID vides)")
