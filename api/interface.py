from api import public, private


# returns: (dict) market for currency pair
#   - top-bid
#   - top-ask
#   - vwap
#   - last-trade
#   - volume
def market(exchange, currency_pair, time_range):
    order_book = public.order_book(currency_pair, group=1)
    top_bid, _ = order_book['bids'][0]
    top_ask, _ = order_book['asks'][0]

    if time_range == 1:
        ticker = public.hourly_ticker(currency_pair)
    else:
        ticker = public.ticker(currency_pair)

    vwap = ticker['vwap']
    last_trade = ticker['last']
    volume = ticker['volume']

    response = {
        'top-bid': str(round(float(top_bid), 1)),
        'top-ask': str(round(float(top_ask), 1)),
        'vwap': str(round(float(vwap), 1)),
        'last-trade': str(round(float(last_trade), 1)),
        'volume': str(round(float(volume), 1)),
    }

    return response

# returns: (dict[]) last 5 trades done on <currency_pair>
#   - side: buy | sell
#   - amount
#   - price
def trades(exchange, currency_pair):
    trades = public.transactions(currency_pair, 'hour')[:5]

    responses = []
    for trade in trades:
        side = 'buy' if trade['type'] == '0' else 'sell'
        amount = trade['amount']
        price = round(float(trade['price']), 1)

        response = {
            'side': side,
            'amount': amount,
            'price': price
        }

        responses.append(response)

    return responses


# returns: (dict[]) all open orders for all currency pairs
#   - side
#   - amount
#   - currency_pair
#   - price
#   - datetime
def open(exchange, currency_pair='all'):
    open_orders = private.open_orders('main', currency_pair)

    responses = []
    for order in open_orders:
        side = 'buy' if order['type'] == '0' else 'sell'
        amount = float(order['amount'])
        currency_pair = order['currency_pair'].lower()
        price = order['price']
        datetime = order['datetime']

        response = {
            'side': side,
            'amount': amount,
            'currency_pair': currency_pair,
            'price': price,
            'datetime': datetime,
        }

        responses.append(response)

    return responses


# returns: (dict) account balance and fees for all currency pairs
#   - <currency_pair>_balance
def balance(exchange):
    account_balance = private.balance('main')
    filtered = { key:value for (key, value) in account_balance.items() if 'balance' in key }

    return filtered

