from telegram.ext import CommandHandler


def help_command(update, context):
    update.message.reply_text("Not yet implemented.")


def generate():
    return CommandHandler('help', help_command)

