from api import public, private


# returns:
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

    ret = {
        'top-bid': str(round(float(top_bid), 1)),
        'top-ask': str(round(float(top_ask), 1)),
        'vwap': str(round(float(vwap), 1)),
        'last-trade': str(round(float(last_trade), 1)),
        'volume': str(round(float(volume), 1)),
    }

    return ret

# returns: last 5 trades done on <currency_pair>
def trades(exchange, currency_pair):
    trades = public.transactions(currency_pair, 'hour')[:5]

    ret = []
    for trade in trades:
        action = 'buy' if trade['type'] == '0' else 'sell'
        amount = trade['amount']
        price = round(float(trade['price']), 1)
        ret.append('{} {} @ {}'.format(action, amount, price))

    return '\n'.join(ret)


# returns: all open orders for all currency pairs
def open(exchange, currency_pair='all'):
    open_orders = private.open_orders('main', currency_pair)
    return open_orders


# returns: account balance and fees for all currency pairs
def balance(exchange):
    account_balance = private.balance('main')
    return account_balance

