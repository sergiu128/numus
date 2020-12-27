import time
import requests


def ticker(currency_pair):
    # params:
    #   currency_pair: currency pair on which to trigger the request
    #
    # returns:
    #   last: last BTC price (last trade)
    #   high: last 24 hours price high
    #   low: last 24 hours price low
    #   vwap: last 24 hours volume weighted average price
    #   volume: last 24 hours volume
    #   bid: highest buy order
    #   ask: lowest sell order
    #   timestamp: unix timestamp date and time
    #   open: first price of the day

    route = 'https://www.bitstamp.net/api/v2/ticker/{}/'.format(currency_pair)

    response = requests.get(route)
    ticker = response.json()

    return ticker



def hourly_ticker(currency_pair):
    # params:
    #   currency_pair: currency pair on which to trigger the request
    #
    # returns:
    #   last: last BTC price (last trade)
    #   high: last 1 hour price high
    #   low: last 1 hour price low
    #   vwap: last 1 hour volume weighted average price
    #   volume: last 1 hour volume
    #   bid: highest buy order
    #   ask: lowest sell order
    #   timestamp: unix timestamp date and time
    #   open: first price of the day

    route = 'https://www.bitstamp.net/api/v2/ticker_hour/{}/'.format(currency_pair)

    response = requests.get(route)
    hourly_ticker = response.json()

    return hourly_ticker


def order_book(currency_pair, group=1):
    # params:
    #   currency_pair: currency pair on which to trigger the request
    #   group:  0 - orders are not grouped at the same price
    #           1 - orders are grouped at the same price
    #           2 - orders with their order ids are not grouped at the same price
    #
    # returns:  a JSON snapshot of the order book with keys: 'bids', 'asks',
    #           'microtimestamp' (when order book was generated),
    #           'timestamp' (when the request was made)
    route = 'https://www.bitstamp.net/api/v2/order_book/{}/'.format(currency_pair)

    payload = {'group': group}
    response = requests.get(route, params=payload)
    order_book = response.json()

    return order_book


def transactions(currency_pair, time_range='day'):
    # params:
    #   currency_pair: currency pair on which to trigger the request
    #   time_range: minute | hour | day
    #
    # returns: all trades done during the last <time_range>
    #   date: unix timestamp date and time
    #   tid: transaction id
    #   price: trade price
    #   amount: executed volume
    #   type: 0 (buy) or 1 (sell)

    if time_range not in ['minute', 'hour', 'day']:
        raise Exception('Invalid time_range. Should be on of: minute, hour, day')

    route = 'https://www.bitstamp.net/api/v2/transactions/{}/'.format(currency_pair)

    payload = {'time': time_range}
    response = requests.get(route, params=payload)
    trades = response.json()

    return trades


def trading_pairs_info():
    # returns: list of trading pairs
    #   name: trading pair
    #   url_symbol: url symbol of trading pair
    #   base_decimals: decimal precision for base currency (BTC/USD - base: BTC).
    #   counter_decimals: decimal precision for counter currency (BTC/USD - counter: USD).
    #   minimum_order: minimum order size
    #   trading: trading engine status (enabled/disabled)
    #   description: trading pair description

    route = 'https://www.bitstamp.net/api/v2/trading-pairs-info/'

    response = requests.get(route)
    info = response.json()

    return info


def ohlc(currency_pair, start=int(time.time()) - 60, end=int(time.time()), step=60, limit=1000):
    # params:
    #   currency_pair: currency pair on which to trigger the request
    #   start: unix timestamp from when OHLC data will be started
    #   end: unix timestamp to when OHLC data will be shown
    #   step: timeframe in seconds; possible options are:
    #         60, 180, 300, 900, 1800, 3600, 7200, 14400, 21600, 43200, 86400, 259200
    #   limit: limit ohlc results (minimum: 1; maximum: 1000)
    #
    # returns:
    #   pair: trading pair on which the request was made
    #   high: price high
    #   timestamp: unix timestamp date and time
    #   volume: volume
    #   low: price low
    #   close: closing price
    #   open: opening price

    if step not in [60, 180, 300, 900, 1800, 3600, 7200, 14400, 21600, 43200, 86400, 259200]:
        raise Exception('Invalid step: {}'.format(step))

    if not (1 <= limit and limit <= 1000):
        raise Exception('Invalid limit: {}'.format(limit))

    route = 'https://www.bitstamp.net/api/v2/ohlc/{}/'.format(currency_pair)

    payload = {
        'currency_pair': currency_pair,
        'start': start,
        'end': end,
        'step': step,
        'limit': limit,
    }
    response = requests.get(route, params=payload)
    ohlc = response.json()

    return ohlc


def eur_usd_rate():
    # returns:
    #   buy: buy conversion rate
    #   sell: sell conversion rate

    route = 'https://www.bitstamp.net/api/eur_usd/'

    response = requests.get(route)
    rate = response.json()

    return rate

