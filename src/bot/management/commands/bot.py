import telebot
# from telebot import types
from django.core.management.base import BaseCommand  # , CommandError
from django.conf import settings
from bot.models import TelegramUser
from pages.models import Page


def bot_command_all(bot, message):
    u = TelegramUser.get_or_update(message.from_user)
    if message.content_type == "location":
        print("latitude='{}' longitude='{}'".format(message.location.latitude, message.location.longitude))
    elif message.content_type == "contact":
        print("contact='{}'".format(message.contact.phone_number))
    elif message.content_type == "text":
        command = message.text.strip()
        if command == "/web":
            msg = u.reset_or_create_webuser_message()
        else:
            try:
                p = Page.objects.get(slug=command)
                msg = p.text
            except Page.DoesNotExist:
                msg = "No entiendo el command '{}'".format(command)
        print("mensaje='{}' reply='{}'".format(message.text.strip(), msg))
        bot.send_message(u.ident, msg, parse_mode="Markdown")
    else:
        print("error", message)


class Command(BaseCommand):
    help = "Bot para telegram"

    def handle(self, *app_labels, **options):

        bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)

        @bot.message_handler(func=lambda message: True, content_types=["text", "location", "contact"])
        def command_all(message):
            return bot_command_all(bot, message)

        print("main loop polling...")
        bot.polling()
