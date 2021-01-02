from bot import config
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
    exchange = context.user_data['exchange']

    accounts = config.accounts(exchange)

    text = []
    for account in accounts:
        text.append('{}:\n  {}\n'.format(account, output(exchange, account)))

    update.message.reply_text(text='\n'.join(text))


def  generate():
    return CommandHandler('balance', _balance)

