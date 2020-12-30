#!/usr/bin/python

import os
import logging
import json

from bot.handlers import (
    market as market_handler,
    help as help_handler,
    trades as trades_handler,
)

from telegram.ext import Updater, CommandHandler

print(__file__)
print(os.path.abspath('config/config.json'))

with open('config/config.json', 'r') as fin:
    config = json.loads(fin.read())

token = config['telegram']['bot_token']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def run():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(market_handler.generate())
    dispatcher.add_handler(help_handler.generate())
    dispatcher.add_handler(trades_handler.generate())

    updater.start_polling()


if __name__ == '__main__':
    run()

