SYMBOLS = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD", "EURJPY", "GBPJPY", "XAUUSD"]
TF_ENTRY, TF_TREND = "M15", "H1"
SCAN_INTERVAL_SEC = 30
MIN_SCORE = 70            # score minimal (0-100) pour signaler/trader
RISK_PER_TRADE = 0.01     # 1 % du capital
SL_ATR, TP_ATR = 1.5, 3.0 # stop / objectif en multiples d'ATR (R:R 1:2)
MAX_SPREAD_ATR = 0.15     # spread max en fraction d'ATR
MAX_OPEN_POSITIONS = 3
DAILY_LOSS_LIMIT = 0.03   # stop trading si -3 % sur la journée
LIVE_TRADING = False      # False = mode signal uniquement (recommandé d'abord en démo)
MAGIC = 260117
# Telegram (créer le bot via @BotFather ; chat id via @userinfobot)
TELEGRAM_TOKEN = ""       # ex: "123456:ABC..."  — ne jamais committer la vraie clé
TELEGRAM_CHAT_ID = ""     # seul ce chat peut piloter l'agent
