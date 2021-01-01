from telegram.ext.commandhandler import CommandHandler
from api import interface


def description():
    return 'get currently open orders'


def open_command(update, context):
    open_orders = interface.open(context.user_data['exchange'], context.user_data['exchange_account'], 'all')

    messages = []
    for order in open_orders:
        message = '{} {} {} @ {}\nplaced at: {}\n'.format(
            order['side'], order['amount'], order['currency_pair'].upper(),
            order['price'], order['datetime']
        )
        messages.append(message)

    update.message.reply_text('\n'.join(messages))


def generate():
    return CommandHandler('open', open_command)

