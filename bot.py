import json
import logging
import requests
from telegram.ext import Updater, CommandHandler


def get_market(symbol):
    resp = requests.get('https://www.bitstamp.net/api/v2/ticker/{}/'.format(symbol))
    ticker = resp.json()

    bid = float(ticker['bid'])
    ask = float(ticker['ask'])
    price = (bid + ask) / 2

    open_price = float(ticker['open'])

    low_price = float(ticker['low'])
    high_price = float(ticker['high'])


    text = 'price: {}\nlow: {}\nhigh: {}\nopen: {}' \
        .format(round(price, 2), round(open_price, 2),
                round(low_price, 2), round(high_price, 2))

    return text


def btc(update, context):
    text = get_market('btceur')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def eth(update, context):
    text = get_market('etheur')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


with open('./.bot_token', 'r') as fin:
    token = fin.read().strip()


updater = Updater(token=token)
dispatcher = updater.dispatcher

btc_handler = CommandHandler('btc', btc)
eth_handler = CommandHandler('eth', eth)
dispatcher.add_handler(btc_handler)
dispatcher.add_handler(eth_handler)

updater.start_polling()
