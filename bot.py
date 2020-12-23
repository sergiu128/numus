#!/usr/bin/python
import sys
import hmac
import json
import time
import uuid
import hashlib
import logging
import requests

from urllib.parse import urlencode
from telegram.ext import Updater, CommandHandler

def load_config():
    with open('./config/config.json', 'r') as config:
        return json.loads(config.read())

config = load_config()

client_id = config['bitstamp']['client_id']
key = config['bitstamp']['key']
secret = config['bitstamp']['secret']

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
    '/api/v2/user_transactions/' + \
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
    'https://www.bitstamp.net/api/v2/user_transactions/',
    headers=headers,
    data=payload_string
)

if not r.status_code == 200:
    raise Exception('Status code not 200')

string_to_sign = (nonce + timestamp + r.headers.get('Content-Type')).encode('utf-8') + r.content
signature_check = hmac.new(API_SECRET, msg=string_to_sign, digestmod=hashlib.sha256).hexdigest()
if not r.headers.get('X-Server-Auth-Signature') == signature_check:
    raise Exception('Signatures do not match')

print(r.content)

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


def btc(update, context):
    text = get_market('btceur')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def eth(update, context):
    text = get_market('etheur')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


token = config['telegram']['bot_token']

updater = Updater(token=token)
dispatcher = updater.dispatcher

btc_handler = CommandHandler('btc', btc)
eth_handler = CommandHandler('eth', eth)
dispatcher.add_handler(btc_handler)
dispatcher.add_handler(eth_handler)

updater.start_polling()
