from telegram.ext.commandhandler import CommandHandler
from api import interface


def describe():
    return 'get currently open orders'


def run(exchange, exchange_account, pair):
    open_orders = interface.open(exchange, exchange_account, pair)

    reply = []
    for order in open_orders:
        message = '{} {} {} @ {}\nplaced at: {}\n'.format(
            order['side'], order['amount'], order['currency_pair'].upper(),
            order['price'], order['datetime']
        )
        reply.append(message)

    return '\n'.join(reply)


def _open(update, context):
    exchange = context.user_data['exchange']
    exchange_account = context.user_data['exchange_account']
    pair = 'all'

    reply = run(exchange, exchange_account, pair)
    update.message.reply_text(reply)


def generate():
    return CommandHandler('open', _open)

