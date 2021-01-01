from bot import keyboard
from bot.handlers import help as help_handler

from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler
from api import interface


SELECT_ACCOUNT, REPLY = range(2)


def select_exchange(update, context):
    markup = keyboard.generate(['bitstamp'])
    update.message.reply_text(text='select exchange:', reply_markup=markup)

    return SELECT_ACCOUNT


def select_account(update, context):
    query = update.callback_query
    query.answer()

    context.user_data['exchange'] = query.data

    markup = keyboard.generate(['main', 'tati'])

    query.edit_message_text(
        text='select account',
        reply_markup=markup
    )

    return REPLY


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
        entry_points=[CommandHandler('set', select_exchange)],
        states={
            SELECT_ACCOUNT: [CallbackQueryHandler(select_account)],
            REPLY: [CallbackQueryHandler(reply)],
        },
        fallbacks=[help_handler.generate()]
    )

    return handler

