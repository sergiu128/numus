from telegram.ext.commandhandler import CommandHandler
from api import interface


def balance_command(update, context):
    account_balance = interface.balance('bitstamp')
    messages = []
    for pair, amount in account_balance.items():
        amount = float(amount)
        if amount > 0.0 and 'balance' in pair:
            currency = pair[:pair.index('_balance')]
            message = '{}: {}'.format(currency.upper(), amount)
            messages.append(message)

    update.message.reply_text('\n'.join(messages))


def  generate():
    return CommandHandler('balance', balance_command)

