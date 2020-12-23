import logging

import api
import util

from telegram.ext import Updater, CommandHandler


config = util.load_config()
token = config['telegram']['bot_token']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def get_btc_market(update, context):
    text = api.get_market('btceur')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def get_eth_market(update, context):
    text = api.get_market('etheur')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def get_open_orders(update, context):
    text = api.get_open_orders('tati')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def run():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    get_btc_market_handler = CommandHandler('btc', get_btc_market)
    get_eth_market_handler = CommandHandler('eth', get_eth_market)
    get_open_orders_handler = CommandHandler('open', get_open_orders)

    dispatcher.add_handler(get_btc_market_handler)
    dispatcher.add_handler(get_eth_market_handler)
    dispatcher.add_handler(get_open_orders_handler)

    updater.start_polling()

