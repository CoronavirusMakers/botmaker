import telebot
import datetime
# from telebot import types
from django.core.management.base import BaseCommand  # , CommandError
from django.conf import settings
from bot.models import TelegramUser
from nodes.models import Node


def check_node(command):
    if not command.startswith("/"):
        return False
    try:
        node = Node.objects.get(slug=command[1:])
    except Node.DoesNotExist:
        return False
    return node.content()


def bot_command_all(bot, message):
    u = TelegramUser.get_or_update(message.from_user)
    if message.content_type == "location":
        print(
            f"latitude='{message.location.latitude}' longitude='{message.location.longitude}'"
        )
    elif message.content_type == "contact":
        print(f"contact='{message.contact.phone_number}'")
    elif message.content_type == "text":
        command = message.text.strip()
        if command == "/web":
            msg = u.reset_or_create_webuser_message()
        else:
            msg = check_node(command) or \
                "No entiendo el command '{}'".format(command)
        print(
            f"{datetime.datetime.now().time()} user='{u.nick}' mensaje={repr(message.text.strip())} reply={repr(msg[:40])}"
        )

        bot.send_message(u.ident, msg, parse_mode="Markdown")
    else:
        print(f"error {message}")


class Command(BaseCommand):
    help = "Bot para telegram"

    def handle(self, *app_labels, **options):

        bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)

        @bot.message_handler(
            func=lambda message: True,
            content_types=["text", "location", "contact"],
        )
        def command_all(message):
            try:
                return bot_command_all(bot, message)
            except Exception as e:
                self.stdout.write(self.style.ERROR("Algo se ha roto :("))
                self.stderr.write(str(e))

        print("main loop polling...")
        bot.polling()
