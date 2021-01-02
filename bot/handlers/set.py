from bot import keyboard
from bot.handlers import help as help_handler

from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler
from api import interface


STATE_GET_ACCOUNT, STATE_REPLY = range(2)


def describe():
    return 'sets the exchange and account to pull data from'


def _state_get_exchange(update, context):
    markup = keyboard.generate(['bitstamp'])
    update.message.reply_text(text='select exchange:', reply_markup=markup)

    return STATE_GET_ACCOUNT


def _state_get_account(update, context):
    query = update.callback_query
    query.answer()

    context.user_data['exchange'] = query.data

    markup = keyboard.generate(['main', 'tati'])

    query.edit_message_text(
        text='select account',
        reply_markup=markup
    )

    return STATE_REPLY


def reply(update, context):
    query = update.callback_query
    query.answer()

    context.user_data['exchange_account'] = query.data

    text = '\n'.join([
        'exchange: {}'.format(context.user_data['exchange']),
        'account: {}'.format(context.user_data['exchange_account']),
    ])

    query.edit_message_text(text=text)

    return ConversationHandler.END


def generate():
    handler = ConversationHandler(
        entry_points=[CommandHandler('set', _state_get_exchange)],
        states={
            STATE_GET_ACCOUNT: [
                CallbackQueryHandler(_state_get_account)
            ],
            STATE_REPLY: [
                CallbackQueryHandler(reply)
            ],
        },
        fallbacks=[help_handler.generate()]
    )

    return handler

