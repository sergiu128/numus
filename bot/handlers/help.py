from telegram.ext import CommandHandler

from bot.handlers import (
    market as market_handler,
    trades as trades_handler,
    open as open_handler,
    balance as balance_handler,
    set as set_handler,
)


def describe():
    raise NotImplementedError()


def run():
    reply = '\n'.join([
        '/market: {}'.format(market_handler.describe()),
        '/trades: {}'.format(trades_handler.describe()),
        '/open: {}'.format(open_handler.describe()),
        '/balance: {}'.format(balance_handler.describe()),
        '/set: {}'.format(set_handler.describe()),
        '/help: display this help prompt',
    ])

    return reply


def callback(update, context):
    reply = run()
    update.message.reply_text(reply)


def generate():
    return CommandHandler('help', callback)

