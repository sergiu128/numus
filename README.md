### numus
A Telegram bot that makes it easier to track your crypto portfolio.

### Commands
- `/market`: get market for a currency pair
- `/trades`: get a list of the last 5 trades
- `/open`: get currently open orders (*requires account key+secret*)
- `/balance`: get account balance for all currency pairs (*requires account key+secret*)
- `/set`: sets the exchange and account to pull data from
- `/timer`:
    - `/timer <command> <time>s/m/h`: trigger a command after `<time>` or every `<time>`
    - `/timer`: cancel one of the active timers
- `/help`: display this help prompt

### Setup
The bot is currently not publicly available, however it only takes 5 minutes to set it up for yourself:
0. run `pip3 install -r requirements.txt`.
1. Contact the [botfather](https://t.me/botfather) and setup up a Telegram bot.
2. Put the bot token in `./config/config.json` (see `./config.json.example`).
3. Run the bot: `python run.py` in your terminal prompt
4. First call `/set`. Now you can now call `/market`, `/trades`, `/help` and `/timer`.
5. Generate an API key and secret for each sub-account on Bitstamp (currently the only supported exchange).
6. Put those in `./config/config.json` (see `./config/config.json.example`). You can now call `/open` and `/balance`.

### Supported Exchanges
- [x] Bitstamp
- [ ] Deribit
- [ ] Gemini
- [ ] Bisq

### Dependecies
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.html).
