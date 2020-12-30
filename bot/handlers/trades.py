from api import interface
from telegram.ext import CommandHandler


def generate():
    return CommandHandler('trades', trades)


def trades(update, context):
    response = interface.trades('bitstamp', 'btceur')
    text = response
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

