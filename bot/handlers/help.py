from telegram.ext import CommandHandler

from bot.handlers import (
    market as market_handler,
    trades as trades_handler,
    open as open_handler,
    balance as balance_handler,
    set as set_handler,
)


def help_command(update, context):
    text = '\n'.join([
        '/market: {}'.format(market_handler.description()),
        '/trades: {}'.format(trades_handler.description()),
        '/open: {}'.format(open_handler.description()),
        '/balance: {}'.format(balance_handler.description()),
        '/set: {}'.format(set_handler.description()),
        '/help: display this help prompt',
    ])

    update.message.reply_text(text=text)


def generate():
    return CommandHandler('help', help_command)

