import os
import logging
import json

from bot.handlers import (
    market as market_handler,
    help as help_handler,
    trades as trades_handler,
)

from telegram.ext import Updater, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class Bot:
    def __init__(self, token):
        self.token = token

    def run(self):
        updater = Updater(token=self.token)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(market_handler.generate())
        dispatcher.add_handler(help_handler.generate())
        dispatcher.add_handler(trades_handler.generate())

        updater.start_polling()

