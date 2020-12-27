import json
import hmac
import time
import uuid
import hashlib
import requests

from urllib.parse import urlencode

import util


config = util.load_config()
client_id = config['bitstamp']['client_id']


def get_user_transactions(account):
    route = '/api/v2/user_transactions/'

    key = config['bitstamp'][account]['key']
    secret = config['bitstamp'][account]['secret']

    api_key = key
    API_SECRET = bytes(secret, 'utf-8')

    timestamp = str(int(round(time.time() * 1000)))
    nonce = str(uuid.uuid4())
    content_type = 'application/x-www-form-urlencoded'
    payload = {'offset': '1'}

    payload_string = urlencode(payload)
    message = \
        'BITSTAMP ' + api_key + \
        'POST' + \
        'www.bitstamp.net' + \
        route + \
        '' + \
        content_type + \
        nonce + \
        timestamp + \
        'v2' + \
        payload_string
    message = message.encode('utf-8')
    signature = hmac.new(API_SECRET, msg=message, digestmod=hashlib.sha256).hexdigest()
    headers = {
        'X-Auth': 'BITSTAMP ' + api_key,
        'X-Auth-Signature': signature,
        'X-Auth-Nonce': nonce,
        'X-Auth-Timestamp': timestamp,
        'X-Auth-Version': 'v2',
        'Content-Type': content_type
    }
    r = requests.post(
        'https://www.bitstamp.net{}'.format(route),
        headers=headers,
        data=payload_string
    )

    if not r.status_code == 200:
        raise Exception('Status code not 200 on route:{} {}'.format(route, r.status_code))

    string_to_sign = (nonce + timestamp + r.headers.get('Content-Type')).encode('utf-8') + r.content
    signature_check = hmac.new(API_SECRET, msg=string_to_sign, digestmod=hashlib.sha256).hexdigest()
    if not r.headers.get('X-Server-Auth-Signature') == signature_check:
        raise Exception('Signatures do not match')

    text = json.loads(r.content)
    return text


def get_open_orders(account):
    route = '/api/v2/open_orders/btceur/'

    key = config['bitstamp'][account]['key']
    secret = config['bitstamp'][account]['secret']

    api_key = key
    API_SECRET = bytes(secret, 'utf-8')

    timestamp = str(int(round(time.time() * 1000)))
    nonce = str(uuid.uuid4())
    content_type = 'application/x-www-form-urlencoded'
    payload = {'offset': '1'}

    payload_string = urlencode(payload)
    message = \
        'BITSTAMP ' + api_key + \
        'POST' + \
        'www.bitstamp.net' + \
        route + \
        '' + \
        content_type + \
        nonce + \
        timestamp + \
        'v2' + \
        payload_string
    message = message.encode('utf-8')
    signature = hmac.new(API_SECRET, msg=message, digestmod=hashlib.sha256).hexdigest()
    headers = {
        'X-Auth': 'BITSTAMP ' + api_key,
        'X-Auth-Signature': signature,
        'X-Auth-Nonce': nonce,
        'X-Auth-Timestamp': timestamp,
        'X-Auth-Version': 'v2',
        'Content-Type': content_type
    }
    r = requests.post(
        'https://www.bitstamp.net{}'.format(route),
        headers=headers,
        data=payload_string
    )

    if not r.status_code == 200:
        raise Exception('Status code not 200 on route:{} {}'.format(route, r.status_code))

    string_to_sign = (nonce + timestamp + r.headers.get('Content-Type')).encode('utf-8') + r.content
    signature_check = hmac.new(API_SECRET, msg=string_to_sign, digestmod=hashlib.sha256).hexdigest()

    if not r.headers.get('X-Server-Auth-Signature') == signature_check:
        raise Exception('Signatures do not match')

    content = json.loads(r.content)

    text = []
    for order in content:
        text.append('{} {}BTC at {} [{}]'.format('buy' if order['type'] == '0' else 'sell', order['amount'], order['price'], order['datetime']))

    return '\n'.join(text)


def get_market(symbol):
    resp = requests.get('https://www.bitstamp.net/api/v2/ticker/{}/'.format(symbol))
    ticker = resp.json()

    bid = float(ticker['bid'])
    ask = float(ticker['ask'])
    price = (bid + ask) / 2

    open_price = float(ticker['open'])

    low_price = float(ticker['low'])
    high_price = float(ticker['high'])

    text = 'price: {}\nlow: {}\nhigh: {}\nopen: {}' \
        .format(round(price, 2), round(open_price, 2),
                round(low_price, 2), round(high_price, 2))

    return text

