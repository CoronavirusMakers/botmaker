import telebot
# from telebot import types
from django.core.management.base import BaseCommand  # , CommandError
from django.conf import settings
from bot.models import TelegramUser
from estatico.models import Pagina


def bot_command_all(bot, message):
    u = TelegramUser.get_or_update(message.from_user)
    if message.content_type == "location":
        print("location=", message.location.latitude, message.location.longitude)
    elif message.content_type == "contact":
        print("contact=", message.contact.phone_number)
    elif message.content_type == "text":
        comando = message.text.strip()
        print(message)
        try:
            p = Pagina.objects.get(slug=comando)
            msg = p.texto
        except Pagina.DoesNotExist:
            msg = "No entiendo el comando {}".format(comando)
        print("mensaje=", message.text.strip(), "reply=", msg)
        bot.send_message(u.ident, msg)
    else:
        print("error", message)


class Command(BaseCommand):
    help = "Importa un extracto de lineas de cajasiete"

    def handle(self, *app_labels, **options):

        bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)

        @bot.message_handler(func=lambda message: True, content_types=["text", "location", "contact"])
        def command_all(message):
            return bot_command_all(bot, message)

        print("main loop polling...")
        bot.polling()
