import datetime
import pytz
import uuid

from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler
)


from bot.handlers import (
    market as market_handler,
    trades as trades_handler,
    open as open_handler,
    balance as balance_handler,
    help as help_handler,
)

from bot import keyboard


STATE_REPLY, STATE_INFO = range(2)

active_timer_jobs = []


def describe():
    return 'use /timer <command> <time>s/m/h) to trigger a command after <time>s/m/h'


def _parse_command(command):
    # TODO check for command validity
    return command


def _parse_count(count):
    if count[-1] not in ['h', 'm', 's']:
        raise Exception('Invalid time unit {}. Use one of: s, m, h.'.format(count[-1]))

    return int(count[:-1]), count[-1]


def _state_get_type(update, context):
    if len(context.args) == 0:
        names = [job.name for job in active_timer_jobs]
        if names == []:
            update.message.reply_text(text='no active timers.')
            return ConversationHandler.END
        else:
            markup = keyboard.generate_currency_pair(names)
            update.message.reply_text(text='active timers, press to remove', reply_markup=markup)
            return STATE_INFO
    elif len(context.args) != 2:
        update.message.reply_text(describe())

        return ConversationHandler.END

    command = _parse_command(context.args[0])
    due, unit = _parse_count(context.args[1])

    if 'timer' not in context.user_data:
        context.user_data['timer'] = {}

    context.user_data['timer']['chat_id'] = update.message.chat_id
    context.user_data['timer']['command'] = command
    context.user_data['timer']['due'] = due
    context.user_data['timer']['unit'] = unit

    markup = keyboard.generate_currency_pair(['once', 'repeat'])
    update.message.reply_text(text='timer type:', reply_markup=markup)

    return STATE_REPLY


def _state_info(update, context):
    query = update.callback_query
    query.answer()

    timer_name = query.data

    for job in active_timer_jobs:
        if job.name == timer_name:
            active_timer_jobs.remove(job)
            break

    query.edit_message_text('timer removed')

    return ConversationHandler.END

def _state_set_timer(update, context):
    query = update.callback_query
    query.answer()

    context.user_data['timer']['type'] = query.data

    chat_id = context.user_data['timer']['chat_id']
    command = context.user_data['timer']['command']
    due = context.user_data['timer']['due']
    unit = context.user_data['timer']['unit']
    timer_type = context.user_data['timer']['type']

    if unit == 's':
        delta = datetime.timedelta(seconds=due)
    elif unit == 'm':
        delta = datetime.timedelta(minutes=due)
    else:
        delta = datetime.timedelta(hours=due)

    callback_context = {
        'chat_id': chat_id,
        'command': command,
        'user_data': context.user_data,
    }

    timer_name = '{}:{}:{}{}'.format(timer_type, command, due, unit)

    timezone = pytz.timezone('Europe/Bucharest')
    if timer_type == 'once':
        when = timezone.localize(datetime.datetime.now() + delta)
        timer_job = context.job_queue.run_once(callback=_callback,
                                               when=when,
                                               context=callback_context,
                                               name=timer_name)
    elif timer_type == 'repeat':
        trigger_time = timezone.localize(datetime.datetime.now())
        timer_job = context.job_queue.run_repeating(callback=_callback,
                                                    interval=delta,
                                                    first=trigger_time,
                                                    context=callback_context,
                                                    name=timer_name)
    else:
        raise Exception('Invalid timer type.')

    active_timer_jobs.append(timer_job)

    query.edit_message_text(
        'timer set: trigger /{} {} {}{}.'.format(
            command,
            'every' if timer_type == 'repeat' else 'after',
            due,
            unit)
    )

    return ConversationHandler.END


def _callback(context):
    # will run the <command> asynchronously once the timer has elapsed
    job = context.job

    chat_id = job.context['chat_id']
    command = job.context['command']
    user_data = job.context['user_data']
    timer_type = user_data['timer']['type']

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

    if timer_type == 'once':
        active_timer_jobs.remove(job)


def generate():
    handler = ConversationHandler(
        entry_points=[CommandHandler('timer', _state_get_type)],
        states={
            STATE_REPLY: [CallbackQueryHandler(_state_set_timer)],
            STATE_INFO: [CallbackQueryHandler(_state_info)]
        },
        fallbacks=[help_handler.generate()]
    )

    return handler

