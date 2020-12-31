from bot import keyboard
from bot.handlers import help as help_handler

from api import interface

from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler
)


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
    text = '{:<12} @ {:>12}\nvwap: {:>17} \nlast-trade: {:>9} \nvolume: {:>13}'.format(
        ''.join(['bid ', response['top-bid']]),
        ''.join([response['top-ask'], ' ask']),
        response['vwap'],
        response['last-trade'],
        response['volume'])

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

