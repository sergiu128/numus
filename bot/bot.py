import logging

from bot.handlers import (
    market as market_handler,
    help as help_handler,
    trades as trades_handler,
    open as open_handler,
    balance as balance_handler,
    set as set_handler,
    timer as timer_handler,
)

from telegram.ext import Updater, PicklePersistence


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class Bot:
    def __init__(self, token):
        self.token = token

        persistence = PicklePersistence(
            'config/bot.pickle',
            store_user_data=True,
            store_bot_data=True,
            single_file=True,
            on_flush=False
        )

        self.updater = Updater(token=self.token, persistence=persistence)
        self.dispatcher = self.updater.dispatcher

    def register_handlers(self):
        self.dispatcher.add_handler(market_handler.generate())
        self.dispatcher.add_handler(help_handler.generate())
        self.dispatcher.add_handler(trades_handler.generate())
        self.dispatcher.add_handler(open_handler.generate())
        self.dispatcher.add_handler(balance_handler.generate())
        self.dispatcher.add_handler(set_handler.generate())
        self.dispatcher.add_handler(timer_handler.generate())

    def run(self):
        self.updater.start_polling()
        self.updater.idle()


