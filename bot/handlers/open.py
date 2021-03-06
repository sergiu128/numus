from bot import config
from telegram.ext.commandhandler import CommandHandler
from api import interface


def describe():
    return 'get currently open orders on all accounts'


def output(exchange, exchange_account, pair):
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

    accounts = config.accounts(exchange)
    if accounts == []:
        update.message.reply_text(text='/open unavailable - no accounts found.')
        return

    text = []
    for account in accounts:
        text.append('{}-{}:\n{}'.format(exchange, account, output(exchange, account, 'all')))

    update.message.reply_text(text='\n'.join(text))


def generate():
    return CommandHandler('open', _open)

