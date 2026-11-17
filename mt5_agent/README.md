# Agent de trading Forex temps réel — MT5

Scanne en continu 10 paires (configurable), note chaque opportunité de 0 à 100
(tendance H1 EMA50/200, alignement EMA20/50 M15, ADX, RSI, pullback, bougie de reprise),
filtre le spread, et peut exécuter avec un risque fixe en % et SL/TP basés sur l'ATR.

## Lancer
```
pip install MetaTrader5 pandas requests  # Windows, terminal MT5 ouvert et connecté
python agent.py
```
`LIVE_TRADING = False` par défaut : signaux seulement. Testez sur compte **démo** avant tout.

## Protections
Risque 1 %/trade, 3 positions max, 1 par symbole, arrêt à -3 % journalier, filtre de spread.

## Outils GitHub recommandés
| Projet | ★ | Usage |
|---|---|---|
| [ariadng/metatrader-mcp-server](https://github.com/ariadng/metatrader-mcp-server) | 852 | MCP : brancher Claude directement sur MT5 |
| [Qoyyuum/mcp-metatrader5-server](https://github.com/Qoyyuum/mcp-metatrader5-server) | 245 | MCP alternatif (données, ordres, historique) |
| [flukelaster/ai-trading-agent](https://github.com/flukelaster/ai-trading-agent) | 79 | Agent Claude + FastAPI + Next.js + MT5 |
| [El-Bach/claude-trader](https://github.com/El-Bach/claude-trader) | 31 | Multi-agents Claude sur EURUSD/XAUUSD… |
| [KVignesh122/MT5-SMC-trading-bot](https://github.com/KVignesh122/MT5-SMC-trading-bot) | 95 | EA MQL5 Smart Money Concepts |
| [masdevid/mt5-quant](https://github.com/masdevid/mt5-quant) | 53 | MCP backtest/optimisation |
| [psyb0t/mt5-httpapi](https://github.com/psyb0t/mt5-httpapi) | 31 | MT5 en VM Docker via REST/MCP (Linux) |

⚠️ Aucun système ne garantit de gains ; le trading à effet de levier peut faire perdre plus que la mise.

## Pilotage depuis le téléphone (Telegram)
1. Sur Telegram, écrivez à **@BotFather** → `/newbot` → copiez la clé dans `TELEGRAM_TOKEN`.
2. Écrivez à **@userinfobot** pour obtenir votre id → `TELEGRAM_CHAT_ID`.
3. Lancez `python agent.py` sur le VPS Windows, puis envoyez `/status` à votre bot.

Commandes : `/start` `/stop` `/live on` `/live off` `/status` `/quit`.
Notifications automatiques : opportunités ★ (max 1/h par signal) et chaque ordre exécuté.
Seul votre chat id est obéi ; les autres messages sont ignorés.
