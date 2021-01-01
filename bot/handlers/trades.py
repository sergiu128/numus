from bot import keyboard
from bot.handlers import help as help_handler

from api import interface

from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler
)


REPLY = 0


def select_currency_pair(update, context):
    markup = keyboard.generate_currency_pair(['btceur', 'etheur'])
    update.message.reply_text(text='currency pair:', reply_markup=markup)

    return REPLY


def reply(update, context):
    query = update.callback_query
    query.answer

    currency_pair = query.data
    trades = interface.trades(context.user_data['exchange'], currency_pair)

    reply = []
    for trade in trades:
        reply.append('{} {} @ {}'.format(trade['side'], trade['amount'], trade['price']))

    query.edit_message_text('\n'.join(reply))

    return ConversationHandler.END


def generate():
    handler = ConversationHandler(
        entry_points=[CommandHandler('trades', select_currency_pair)],
        states = {
            REPLY: [CallbackQueryHandler(reply)]
        },
        fallbacks=[help_handler.generate()]
    )

    return handler

