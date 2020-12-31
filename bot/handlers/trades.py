from api import interface
from telegram.ext import CommandHandler


def trades(update, context):
    trades = interface.trades('bitstamp', 'btceur')

    reply = []
    for trade in trades:
        reply.append('{} {} @ {}'.format(trade['side'], trade['amount'], trade['price']))

    update.message.reply_text('\n'.join(reply))


def generate():
    return CommandHandler('trades', trades)
