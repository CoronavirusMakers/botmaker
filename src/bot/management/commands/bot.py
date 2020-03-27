import telebot
import datetime
# from telebot import types
from django.core.management.base import BaseCommand  # , CommandError
from django.conf import settings
from bot.models import TelegramUser
from pages.models import Page
from geolinks.models import Place

def check_place(command):
    if not command.startswith("/"):
        return False
    try:
        place = Place.objects.get(slug=command[1:])
    except Place.DoesNotExist:
        return False
    return place.content()


def check_page(command):
    try:
        p = Page.objects.get(slug=command)
    except Page.DoesNotExist:
        return False
    return p.text


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
        elif command == "/world":
            msg = Place.all_content()
        else:
            msg = check_place(command) or check_page(command) or \
                "No entiendo el command '{}'".format(command)
        print("{} user='{}' mensaje={} reply={}".format(
            datetime.datetime.now().time(), 
            u.nick, repr(message.text.strip()), repr(msg[:40])))
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
