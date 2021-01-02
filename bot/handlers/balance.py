from api import interface
from telegram.ext.commandhandler import CommandHandler


def describe():
    return 'get account balance for all currency pairs'


def output(exchange, exchange_account):
    account_balance = interface.balance(exchange, exchange_account)

    reply = []
    for pair, amount in account_balance.items():
        amount = float(amount)
        if amount > 0.0 and 'balance' in pair:
            currency = pair[:pair.index('_balance')]
            reply.append('{}: {}'.format(currency.upper(), amount))

    return '\n'.join(reply)


def _balance(update, context):
    # TODO add option to return balance for all accounts
    exchange = context.user_data['exchange']
    exchange_account = context.user_data['exchange_account']

    text = output(exchange, exchange_account)

    update.message.reply_text(text=text)


def  generate():
    return CommandHandler('balance', _balance)

