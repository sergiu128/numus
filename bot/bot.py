#!/usr/bin/python
import logging
import json

import api.public
import api.interface

from telegram.ext import Updater, CommandHandler


with open('../config/config.json', 'r') as fin:
    config = json.loads(fin.read())

token = config['telegram']['bot_token']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def market(update, context):
    response = api.interface.market('bitstamp', 'btceur')
    text = '{:<12} @ {:>12}\nvwap: {:>17} \nlast-trade: {:>9} \nvolume: {:>13}'.format(
        ''.join(['bid ', response['top-bid']]),
        ''.join([response['top-ask'], ' ask']),
        response['top-ask'],
        response['vwap'],
        response['last-trade'],
        response['volume'])

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def run():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    market_handler = CommandHandler('market', market)

    dispatcher.add_handler(market_handler)

    updater.start_polling()

if __name__ == '__main__':
    run()

