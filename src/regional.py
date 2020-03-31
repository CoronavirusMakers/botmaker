#!/usr/bin/env python3

import telebot
import json
import os
from decouple import config


class settings:
    TELEGRAM_TOKEN = config('REGIONAL_TELEGRAM_TOKEN')
    ADMINS = config("REGIONAL_ADMINS", cast=lambda v: json.loads(v))
    BOT_NAME = config("REGIONAL_BOT_NAME")


def format_user(user):
    msg = f"{user.first_name} {user.last_name}"
    msg += f" @{user.username}" if user.username else f" @{user.id}"
    return msg


class PersistDict(dict):
    def __init__(self, filename):
        self._filename = filename
        if os.path.exists(filename):
            d = json.load(open(filename))
            super().__init__(**d)

    def save(self):
        json.dump(self, open(self._filename, "w"))


lista_de_chats = PersistDict("regional.json")
lista_de_chats.save()


def bot_command_all(bot, message):
    text = message.text.strip() if message.text else ""
    if message.content_type == "new_chat_members":
        if message.new_chat_member.username == settings.BOT_NAME:
            group_id = message.chat.id
            group_title = message.chat.title
            print(f"Entro en grupo {group_title}")
            lista_de_chats[group_id] = group_title
            lista_de_chats.save()
        else:
            print(f"Ignorando mensaje de {message.new_chat_member.username}")
    elif message.content_type == "left_chat_member":
        if message.left_chat_member.username == settings.BOT_NAME:
            group_id = message.chat.id
            group_title = message.chat.title
            print(f"Salgo de grupo {group_title}")
            if group_id in lista_de_chats:
                del lista_de_chats[group_id]
                lista_de_chats.save()
        else:
            print(f"Ignorando mensaje2 de {message.left_chat_member.username}")
    elif message.content_type == "text":
        group_title = message.chat.title
        from_user = format_user(message.from_user)
        if message.chat.type == "group":  # mensaje desde grupo
            if message.reply_to_message:
                for id_, username in settings.ADMINS.items():  # mensaje de broadcast
                    print(f"Enviando de grupo {group_title} a {username}")
                    bot.send_message(id_, f"{from_user} en {group_title}:\n{text}")
            else:
                print(f"Ignorando de grupo {group_title} {text}")

        elif message.chat.type == "private":  # mensaje desde usuario
            if message.from_user.username in settings.ADMINS.values():  # mensaje de broadcast
                print(f"Enviando broadcast {text}")
                for group_id, group_title in lista_de_chats.items():
                    bot.forward_message(group_id, message.from_user.id, message.message_id)
                    bot.send_message(message.from_user.id, f"Reenviado a grupo {group_title}")
            else:
                bot.send_message(message.from_user.id, "Lo siento, no entiendo")
                print(f"Ignorando {format_user(message.from_user)} {text}")
    else:
        print(f"Mensaje desconocido {message}")


bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)


@bot.message_handler(content_types=["text", "new_chat_members", "left_chat_member"])
def command_all(message):
    try:
        return bot_command_all(bot, message)
    except Exception as e:
        print("Algo se ha roto :(")
        print(f"{e.__class__.__name__}: {e}")


print("main loop polling...")
bot.polling()
