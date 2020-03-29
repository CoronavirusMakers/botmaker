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
    time = datetime.datetime.now().time()
    from_text = message.text.strip()
    to_id = u.ident
    if message.content_type == "location":
        print(
            f"latitude='{message.location.latitude}' longitude='{message.location.longitude}'"
        )
    elif message.content_type == "contact":
        print(f"contact='{message.contact.phone_number}'")
    elif message.content_type == "text":
        reply = message.reply_to_message
        if reply:
            if u.receive_unknown and "forward_from" in reply.json and 'text' in reply.json:
                from_text = reply.json['text']
                to_id = reply.json["forward_from"]["id"]
                to_text = message.text
                to = TelegramUser.objects.get(ident=to_id)
                bot.send_message(to_id, to_text)
                for tu in TelegramUser.objects.filter(receive_unknown=True):
                    if tu != u:
                        bot.send_message(tu.ident, f"De {u.nick} a {to.nick}: {to_text}")
                print(f"{time} user='{u.nick}' mensaje={repr(from_text)} reply1={repr(to_text[:40])}")
            else:
                print(f"{time} user='{u.nick}' mensaje={repr(from_text)} ignoring")
        else:
            command = message.text.strip()
            if command == "/web":
                to_text = u.reset_or_create_webuser_message()
                print(f"{time} user='{u.nick}' mensaje={repr(from_text)} reply2={repr(to_text[:40])}")
                bot.send_message(to_id, to_text, parse_mode="Markdown")
            elif command.startswith("/"):
                to_text = check_node(command) or \
                    "No entiendo el command '{}'".format(command)
                print(f"{time} user='{u.nick}' mensaje={repr(from_text)} reply3={repr(to_text[:40])}")
                bot.send_message(to_id, to_text, parse_mode="Markdown")
            elif not u.receive_unknown:
                for tu in TelegramUser.objects.filter(receive_unknown=True):
                    bot.forward_message(tu.ident, message.from_user.id, message.message_id)
                print(f"{time} user='{u.nick}' mensaje={repr(from_text)} forwarding to admins")
            else:
                print(f"{time} user='{u.nick}' mensaje={repr(from_text)} ignoring admin")

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
                self.stderr.write(f"{e.__class__.__name__}: {e}")

        print("main loop polling...")
        bot.polling()
