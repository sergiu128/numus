import datetime
import pytz
from telegram.ext import CommandHandler

from bot.handlers import (
    market as market_handler,
    trades as trades_handler,
    open as open_handler,
    balance as balance_handler,
)


def describe():
    return 'use /timer <command> <time>s/m/h) to trigger a command after <time>s/m/h'


def _parse_command(command):
    # TODO check for command validity
    return command


def _parse_count(count):
    if count[-1] not in ['h', 'm', 's']:
        raise Exception('Invalid time unit {}. Use one of: s, m, h.'.format(count[-1]))

    return int(count[:-1]), count[-1]


def _callback(context):
    # will run the <command> asynchronously once the timer has elapsed
    job = context.job

    chat_id = job.context['chat_id']
    command = job.context['command']
    user_data = job.context['user_data']

    if command == 'market':
        pooled_function = market_handler.run
        pooled_args = {
            'exchange': user_data['exchange'],
            'currency_pair': user_data['market']['currency_pair'],
            'time_range': user_data['market']['time_range']
        }
    elif command == 'trades':
        pooled_function = trades_handler.run
        pooled_args = {
            'exchange': user_data['exchange'],
            'currency_pair': user_data['trades']['currency_pair'],
        }
    elif command == 'open':
        pooled_function = open_handler.run
        pooled_args = {
            'exchange': user_data['exchange'],
            'exchange_account': user_data['exchange_account'],
            'pair': 'all',
        }
    elif command == 'balance':
        pooled_function = balance_handler.run
        pooled_args = {
            'exchange': user_data['exchange'],
            'exchange_account': user_data['exchange_account'],
        }
    else:
        raise NotImplementedError()

    promise = context.dispatcher.run_async(pooled_function, **pooled_args)
    promise.run()
    context.bot.send_message(chat_id=chat_id, text=promise.result())


def _timer(update, context):
    if len(context.args) != 2:
        update.message.reply_text(describe())
        return

    command = _parse_command(context.args[0])
    due, unit = _parse_count(context.args[1])

    if unit == 's':
        delta = datetime.timedelta(seconds=due)
    elif unit == 'm':
        delta = datetime.timedelta(minutes=due)
    else:
        delta = datetime.timedelta(hours=due)

    timezone = pytz.timezone('Europe/Bucharest')
    when = timezone.localize(datetime.datetime.now() + delta)

    callback_context = {
        'chat_id': update.message.chat_id,
        'command': command,
        'user_data': context.user_data,
    }

    context.job_queue.run_once(_callback, when, context=callback_context, name=str(update.message.chat_id))

    update.message.reply_text('timer set: trigger /{} after {}{}.'.format(command, due, unit))


def generate():
    return CommandHandler('timer', _timer)

