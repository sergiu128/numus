import os
import logging
import json

from bot.handlers import (
    market as market_handler,
    help as help_handler,
    trades as trades_handler,
    open as open_handler,
    balance as balance_handler,
)

from telegram.ext import Updater, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class Bot:
    def __init__(self, token):
        self.token = token

    def register_handlers(self):
        self.updater = Updater(token=self.token)
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_handler(market_handler.generate())
        self.dispatcher.add_handler(help_handler.generate())
        self.dispatcher.add_handler(trades_handler.generate())
        self.dispatcher.add_handler(open_handler.generate())
        self.dispatcher.add_handler(balance_handler.generate())

    def run(self):
        self.updater.start_polling()

