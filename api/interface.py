import json
from api import public

# returns:
#   - top-bid
#   - top-ask
#   - vwap
#   - last-trade
#   - volume
def market(exchange, currency_pair):
    order_book = public.order_book(currency_pair, group=1)
    top_bid, _ = order_book['bids'][0]
    top_ask, _ = order_book['asks'][0]

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
