#!/usr/bin/python

import json
from bot import bot

import api.private

with open('config/config.json', 'r') as fin:
    config = json.loads(fin.read())

if __name__ == '__main__':
    bot = bot.Bot(config['telegram']['bot_token'])
    bot.run()

