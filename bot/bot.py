#!/usr/bin/python

import logging
import json

import api.public
import api.interface

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


with open('../config/config.json', 'r') as fin:
    config = json.loads(fin.read())

token = config['telegram']['bot_token']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def market(update, context):
    keyboard = [
        [
            InlineKeyboardButton("24h", callback_data='24'),
            InlineKeyboardButton("1h", callback_data='1'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('time range:', reply_markup=reply_markup)


def market_callback(update, context):
    query = update.callback_query

    query.answer()

    if query.data == '24' or query.data == '1':
        time_range = int(query.data)
    else:
        raise Exception('Invalid time range.')

    response = api.interface.market('bitstamp', 'btceur', time_range)
    text = '{:<12} @ {:>12}\nvwap: {:>17} \nlast-trade: {:>9} \nvolume: {:>13}'.format(
        ''.join(['bid ', response['top-bid']]),
        ''.join([response['top-ask'], ' ask']),
        response['vwap'],
        response['last-trade'],
        response['volume'])

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def trades(update, context):
    response = api.interface.trades('bitstamp', 'btceur')
    text = response
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def help_command(update, context) -> None:
    update.message.reply_text("Not yet implemented.")


def run():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('help', help_command))

    dispatcher.add_handler(CommandHandler('market', market))
    dispatcher.add_handler(CallbackQueryHandler(market_callback))

    dispatcher.add_handler(CommandHandler('trades', trades))

    updater.start_polling()

if __name__ == '__main__':
    run()

