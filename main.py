#!/usr/bin/python

import json
from bot import bot


with open('config/config.json', 'r') as config:
    config = json.loads(config.read())


if __name__ == '__main__':
    bot = bot.Bot(config['telegram']['bot_token'])
    bot.run()

