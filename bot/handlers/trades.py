from bot import keyboard
from bot.handlers import help as help_handler

from api import interface

from telegram.ext import (
    ChosenInlineResultHandler,
    Handler,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler
)


STATE_REPLY = 0


def describe():
    return 'get a list of the last 5 trades'


def run(exchange, currency_pair):
    trades = interface.trades(exchange, currency_pair)

    reply = []
    for trade in trades:
        reply.append('{} {} @ {}'.format(trade['side'], trade['amount'], trade['price']))

    return '\n'.join(reply)

def _state_get_currency_pair(update, context):

    markup = keyboard.generate_currency_pair(['btceur', 'etheur'])
    update.message.reply_text(text='currency pair:', reply_markup=markup)

    return STATE_REPLY


def _state_reply(update, context):
    query = update.callback_query
    query.answer()

    exchange = context.user_data['exchange']
    currency_pair = query.data

    reply = run(exchange, currency_pair)
    query.edit_message_text(reply)

    return ConversationHandler.END


def generate():
    handler = ConversationHandler(
        entry_points=[CommandHandler('trades', _state_get_currency_pair)],
        states = {
            STATE_REPLY: [CallbackQueryHandler(_state_reply)]
        },
        fallbacks=[help_handler.generate()]
    )

    return handler

