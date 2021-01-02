from bot import keyboard
from bot.handlers import help as help_handler

from api import interface

from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler
)


STATE_GET_TIME, STATE_REPLY = range(2)


def describe():
    return 'get market for a currency pair'


def output(exchange, currency_pair, time_range):
    response = interface.market(exchange, currency_pair, time_range)

    bid_ask_spread = '{:<12} @ {:>12}'.format(
        ''.join(['bid ', response['top-bid']]),
        ''.join([response['top-ask'], ' ask']))
    last_trade = 'last trade: {:>9}'.format(response['last-trade'])
    day_open = 'day-open: {:>9}'.format(response['day-open'])

    vwap = '{}h vwap: {:>12}'.format(time_range, response['vwap'])
    low = '{}h low: {:>15}'.format(time_range, response['low'])
    high = '{}h high: {:>14}'.format(time_range, response['high'])
    volume = '{}h volume: {:>8}'.format(time_range, response['volume'])

    text = '\n'.join([bid_ask_spread, '', last_trade, day_open, '', vwap, low, high, volume])

    return text


def _state_0_get_currency_pair(update, context):
    if 'market' not in context.user_data:
        context.user_data['market'] = {}

    markup = keyboard.generate_currency_pair(['btceur', 'etheur'])
    update.message.reply_text(text='currency pair:', reply_markup=markup)

    return STATE_GET_TIME


def _state_1_get_time(update, context):
    query = update.callback_query
    query.answer()

    context.user_data['market']['currency_pair'] = query.data
    markup = keyboard.generate_time(['24h', '1h'])
    query.edit_message_text(text='time range:', reply_markup=markup)

    return STATE_REPLY


def _state_2_reply(update, context):
    query = update.callback_query
    query.answer()

    if query.data == '24' or query.data == '1':
        context.user_data['market']['time_range'] = int(query.data)
    else:
        raise Exception('Invalid time range.')

    exchange = context.user_data['exchange']
    currency_pair = context.user_data['market']['currency_pair']
    time_range = context.user_data['market']['time_range']

    text = output(exchange, currency_pair, time_range)
    query.edit_message_text(text=text)

    return ConversationHandler.END


def generate():
    handler = ConversationHandler(
        entry_points=[
            CommandHandler('market', _state_0_get_currency_pair)
        ],
        states={
            STATE_GET_TIME: [CallbackQueryHandler(_state_1_get_time)],
            STATE_REPLY: [CallbackQueryHandler(_state_2_reply)]
        },
        fallbacks=[help_handler.generate()],
    )

    return handler

