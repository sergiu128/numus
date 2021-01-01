from bot import keyboard
from bot.handlers import help as help_handler

from api import interface

from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler
)

from telegram.parsemode import ParseMode


SELECT, REPLY = range(2)


def select_currency_pair(update, context):
    markup = keyboard.generate_currency_pair(['btceur', 'etheur'])

    update.message.reply_text('currency pair:', reply_markup=markup)

    return SELECT


def select_time(update, context):
    query = update.callback_query
    query.answer()

    context.user_data['currency_pair'] = query.data

    markup = keyboard.generate_time(['24h', '1h'])

    query.edit_message_text(
        text='time range:', reply_markup=markup
    )

    return REPLY


def reply(update, context):
    query = update.callback_query

    query.answer()

    if query.data == '24' or query.data == '1':
        time_range = int(query.data)
    else:
        raise Exception('Invalid time range.')

    currency_pair = context.user_data['currency_pair']

    response = interface.market('bitstamp', currency_pair, time_range)

    bid_ask_spread = '{:<12} @ {:>12}'.format(
        ''.join(['bid ', response['top-bid']]),
        ''.join([response['top-ask'], ' ask'])
    )
    last_trade = 'last trade: {:>9}'.format(response['last-trade'])
    day_open = 'day-open: {:>9}'.format(response['day-open'])

    vwap = '{}h vwap: {:>12}'.format(time_range, response['vwap'])
    low = '{}h low: {:>15}'.format(time_range, response['low'])
    high = '{}h high: {:>14}'.format(time_range, response['high'])
    volume = '{}h volume: {:>8}'.format(time_range, response['volume'])

    text = '\n'.join([bid_ask_spread, '', last_trade, day_open, '', vwap, low, high, volume])

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    return ConversationHandler.END


def generate():
    handler = ConversationHandler(
        entry_points=[CommandHandler('market', select_currency_pair)],
        states = {
            SELECT: [
                CallbackQueryHandler(select_time)
            ],
            REPLY: [
                CallbackQueryHandler(reply)
            ]
        },
        fallbacks=[help_handler.generate()],
    )

    return handler

