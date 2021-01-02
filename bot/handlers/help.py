from telegram.ext import CommandHandler

from bot.handlers import (
    market as market_handler,
    trades as trades_handler,
    open as open_handler,
    balance as balance_handler,
    set as set_handler,
    timer as timer_handler,
)


def describe():
    raise NotImplementedError()


def output():
    # TODO figure out a better way to write this
    timer_description = timer_handler.describe()

    reply = '\n\n'.join([
        '/market: {}'.format(market_handler.describe()),
        '/trades: {}'.format(trades_handler.describe()),
        '/open: {}'.format(open_handler.describe()),
        '/balance: {}'.format(balance_handler.describe()),
        '/set: {}'.format(set_handler.describe()),
        timer_description[0],
        timer_description[1],
        '/help: display this help prompt',
    ])

    return reply


def _callback(update, context):
    text = output()
    update.message.reply_text(text=text)


def generate():
    return CommandHandler('help', _callback)

