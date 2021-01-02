from bot import keyboard, config
from bot.handlers import help as help_handler

from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler
from api import interface


STATE_GET_ACCOUNT, STATE_REPLY = range(2)


def describe():
    return 'sets the exchange and account to pull data from'


def output(exchange, exchange_account):
    text = '\n'.join([
        'exchange: {}'.format(exchange),
        'account: {}'.format(exchange_account),
    ])

    return text


def _state_0_get_exchange(update, context):
    markup = keyboard.generate(config.exchanges())
    update.message.reply_text(text='select exchange:', reply_markup=markup)

    return STATE_GET_ACCOUNT


def _state_1_get_account(update, context):
    query = update.callback_query
    query.answer()

    exchange = query.data
    context.user_data['exchange'] = exchange

    markup = keyboard.generate(config.accounts(exchange))

    query.edit_message_text(
        text='select account',
        reply_markup=markup
    )

    return STATE_REPLY


def _state_2_reply(update, context):
    query = update.callback_query
    query.answer()

    context.user_data['exchange_account'] = query.data

    exchange = context.user_data['exchange']
    exchange_account = context.user_data['exchange_account']

    text = output(exchange, exchange_account)

    query.edit_message_text(text=text)

    return ConversationHandler.END


def generate():
    handler = ConversationHandler(
        entry_points=[CommandHandler('set', _state_0_get_exchange)],
        states={
            STATE_GET_ACCOUNT: [
                CallbackQueryHandler(_state_1_get_account)
            ],
            STATE_REPLY: [
                CallbackQueryHandler(_state_2_reply)
            ],
        },
        fallbacks=[help_handler.generate()]
    )

    return handler

