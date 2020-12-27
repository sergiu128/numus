import time
import pytest
from api import public


def test_ticker():
    ticker = public.ticker('btceur')

    assert 'last' in ticker
    assert 'high' in ticker
    assert 'low' in ticker
    assert 'vwap' in ticker
    assert 'volume' in ticker
    assert 'bid' in ticker
    assert 'ask' in ticker
    assert 'timestamp' in ticker
    assert 'open' in ticker


def test_hourly_ticker():
    ticker = public.hourly_ticker('btceur')

    assert 'last' in ticker
    assert 'high' in ticker
    assert 'low' in ticker
    assert 'vwap' in ticker
    assert 'volume' in ticker
    assert 'bid' in ticker
    assert 'ask' in ticker
    assert 'timestamp' in ticker
    assert 'open' in ticker


def test_order_book():
    order_book = public.order_book('btceur', group=0)

    assert 'bids' in order_book
    assert 'asks' in order_book
    assert 'microtimestamp' in order_book
    assert 'timestamp' in order_book
    assert len(order_book['bids'][0]) == 2

    order_book = public.order_book('btceur', group=1)
    assert 'bids' in order_book
    assert 'asks' in order_book
    assert 'microtimestamp' in order_book
    assert 'timestamp' in order_book
    assert len(order_book['bids'][0]) == 2



    order_book = public.order_book('btceur', group=2)
    assert 'bids' in order_book
    assert 'asks' in order_book
    assert 'microtimestamp' in order_book
    assert 'timestamp' in order_book
    # also contains the order id
    assert len(order_book['bids'][0]) == 3


def test_transactions():
    transactions = public.transactions('btceur', time_range='minute')

    if len(transactions) > 0:
        transaction = transactions[0]

        assert 'date' in transaction
        assert 'tid' in transaction
        assert 'price' in transaction
        assert 'amount' in transaction
        assert 'type' in transaction
        assert transaction['type'] == '0' or transaction['type'] == '1'

    with pytest.raises(Exception):
        transactions = public.transactions('btceur', time_range='foobar')


def test_trading_pairs_info():
    pairs = public.trading_pairs_info()

    if len(pairs) > 0:
        pair = pairs[0]
        assert 'name' in pair
        assert 'url_symbol' in pair
        assert 'base_decimals' in pair
        assert 'counter_decimals' in pair
        assert 'minimum_order' in pair
        assert 'trading' in pair
        assert 'description' in pair

    # TODO: hardcode test against all known trading pairs


def test_ohlc():
    result = public.ohlc('btceur')
    
    assert 'data' in result
    data = result['data']

    assert 'pair' in data
    assert 'ohlc' in data
    ohlc = data['ohlc']

    if len(ohlc) > 0:
        sample = ohlc[0]
        assert 'high' in sample
        assert 'timestamp' in sample
        assert 'volume' in sample
        assert 'low' in sample
        assert 'close' in sample
        assert 'open' in sample

    with pytest.raises(Exception):
        public.ohlc('btceur', start=int(time.time()) - 60, end=int(time.time()), step=10)


def test_eur_usd_rate():
    rate = public.eur_usd_rate()

    assert 'sell' in rate
    assert 'buy' in rate
