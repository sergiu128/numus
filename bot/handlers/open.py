from telegram.ext.commandhandler import CommandHandler
from api import interface


def open_command(update, context):
    open_orders = interface.open('bitstamp', 'all')

    [{"price":"21000.00","currency_pair":"BTC\/EUR","datetime":"2020-12-31 10:42:43","amount":"0.33679172","type":"0","id":"1313080886763520"}]

    messages = []
    for order in open_orders:
        side = 'buy' if order['type'] == '0' else 'sell'
        amount = float(order['amount'])
        currency_pair = order['currency_pair'].lower()
        price = order['price']
        date = order['datetime']

        message = '{} {} {} @ {}\nplaced at: {}\n'.format(side, amount, currency_pair, price, date)
        messages.append(message)

    update.message.reply_text('\n'.join(messages))


def generate():
    return CommandHandler('open', open_command)
