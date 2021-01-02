import json


with open('config/config.json', 'r') as fin:
    config = json.loads(fin.read())


def exchanges():
    return list(config['exchanges'].keys())


def accounts(exchange):
    if exchange not in exchanges():
        raise Exception('Invalid exchange {}.'.format(exchange))

    return list(config['exchanges'][exchange]['accounts'].keys())


def account(exchange, account):
    if exchange not in exchanges():
        raise Exception('Invalid exchange {}.'.format(exchange))

    if account not in accounts(exchange):
        raise Exception('Invalid exchange account {}.'.format(account))

    return config['exchanges'][exchange]['accounts'][account]

