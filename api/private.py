import json
import hmac
import time
import uuid
import hashlib
import requests

from urllib.parse import urlencode


def user_transactions(account, limit):
    route = '/api/v2/user_transactions/'
    payload = {
        'limit': str(limit)
    }

    response = _query(account, route, payload)
    return response


def open_orders(account, currency_pair):
    route = '/api/v2/open_orders/{}/'.format(currency_pair)

    response = _query(account, route, {})
    return response


def order_status(account, offset, order_id):
    route = '/api/v2/order_status/'
    payload = {
        'offset': str(offset),
        'id': str(order_id)
    }

    response = _query(account, route, payload)
    return response


with open('config/config.json', 'r') as fin:
    config = json.loads(fin.read())


def _query(account, route, payload):
    print('here payload {}'.format(payload))
    key = config['bitstamp'][account]['key']
    secret = bytes(config['bitstamp'][account]['secret'], 'utf-8')
    nonce = str(uuid.uuid4())
    timestamp = str(int(round(time.time() * 1000)))

    payload_string, content_type = '', ''
    if payload != {}:
        payload_string = urlencode(payload)
        content_type = 'application/x-www-form-urlencoded'

    message = 'BITSTAMP {}POSTwww.bitstamp.net{}{}{}{}v2{}'\
        .format(key, route, content_type, nonce, timestamp, payload_string)\
        .encode('utf-8')

    signature = hmac.new(secret, msg=message, digestmod=hashlib.sha256).hexdigest()

    headers = {
        'X-Auth': 'BITSTAMP {}'.format(key),
        'X-Auth-Signature': signature,
        'X-Auth-Nonce': nonce,
        'X-Auth-Timestamp': timestamp,
        'X-Auth-Version': 'v2',
    }

    print(content_type)
    if content_type != '':
        headers['Content-Type'] = content_type

    response = requests.post(
        'https://www.bitstamp.net{}'.format(route),
        headers=headers,
        data=payload_string
    )

    if not response.status_code == 200:
        raise Exception('Status code not 200 on route:{} {}'.format(route, response.status_code))

    if response.reason != 'OK':
        raise Exception('Invalid {} call; reason: {}'.format(route, response.reason))

    content_type = response.headers.get('Content-Type')
    if content_type is None:
        raise Exception('Cannot get Content-Type response header.')

    string_to_sign = (nonce + timestamp + content_type).encode('utf-8') + response.content
    signature_check = hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).hexdigest()

    if not response.headers.get('X-Server-Auth-Signature') == signature_check:
        raise Exception('Signatures do not match')

    content = json.loads(response.content)

    return content

