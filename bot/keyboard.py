import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def generate_currency_pair(pairs):
    keyboard = []
    for pair in pairs:
        keyboard.append([InlineKeyboardButton(pair, callback_data=pair)])

    return InlineKeyboardMarkup(keyboard)

def generate_time(times):
    pattern = re.compile('[0-9]+')

    keyboard = []
    for t in times:
        match = pattern.match(t)
        if match is None:
            raise Exception('Invalid time.')

        keyboard.append([InlineKeyboardButton(t, callback_data=match.group())])

    return InlineKeyboardMarkup(keyboard)

