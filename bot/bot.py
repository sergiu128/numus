#!/usr/bin/python

import re
import logging
import json

from telegram.utils.types import ConversationDict

import api.public
import api.interface

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler


SELECT_TIME = 'select-time'
MARKET_REPLY = 'market-callback'

with open('../config/config.json', 'r') as fin:
    config = json.loads(fin.read())

token = config['telegram']['bot_token']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class Keyboard:
    @staticmethod
    def currency_pair(pairs):
        keyboard = []
        for pair in pairs:
            keyboard.append([InlineKeyboardButton(pair, callback_data=pair)])

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def time(times):
        pattern = re.compile('[0-9]+')

        keyboard = []
        for t in times:
            match = pattern.match(t)
            if match is None:
                raise Exception('Invalid time.')

            keyboard.append([InlineKeyboardButton(t, callback_data=match.group())])

        return InlineKeyboardMarkup(keyboard)


def market_select_pair(update, context):
    keyboard = Keyboard.currency_pair(['btceur', 'etheur'])

    update.message.reply_text('time range:', reply_markup=keyboard)

    return SELECT_TIME


def market_select_time(update, context):
    query = update.callback_query
    query.answer()

    context.user_data['currency_pair'] = query.data

    keyboard = Keyboard.time(['24h', '1h'])

    query.edit_message_text(
        text='time range:', reply_markup=keyboard
    )

    return MARKET_REPLY


def market_reply(update, context):
    query = update.callback_query

    query.answer()

    if query.data == '24' or query.data == '1':
        time_range = int(query.data)
    else:
        raise Exception('Invalid time range.')

    currency_pair = context.user_data['currency_pair']

    response = api.interface.market('bitstamp', currency_pair, time_range)
    text = '{:<12} @ {:>12}\nvwap: {:>17} \nlast-trade: {:>9} \nvolume: {:>13}'.format(
        ''.join(['bid ', response['top-bid']]),
        ''.join([response['top-ask'], ' ask']),
        response['vwap'],
        response['last-trade'],
        response['volume'])

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    return ConversationHandler.END


def trades(update, context):
    response = api.interface.trades('bitstamp', 'btceur')
    text = response
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def help_command(update, context) -> None:
    update.message.reply_text("Not yet implemented.")


def run():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher


    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('market', market_select_pair)],
        states = {
            SELECT_TIME: [
                CallbackQueryHandler(market_select_time)
            ],
            MARKET_REPLY: [
                CallbackQueryHandler(market_reply)
            ]
        },
        fallbacks=[CommandHandler('help', help_command)],
    )

    dispatcher.add_handler(conversation_handler)
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('trades', trades))

    updater.start_polling()

if __name__ == '__main__':
    run()

