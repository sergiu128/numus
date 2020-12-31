from api import interface
from telegram.ext.commandhandler import CommandHandler


def balance_command(update, context):
    account_balance = interface.balance('bitstamp')
    reply = []
    for pair, amount in account_balance.items():
        amount = float(amount)
        if amount > 0.0 and 'balance' in pair:
            currency = pair[:pair.index('_balance')]
            reply.append(
                '{}: {}'.format(currency.upper(), amount)
            )

    update.message.reply_text('\n'.join(reply))


def  generate():
    return CommandHandler('balance', balance_command)

