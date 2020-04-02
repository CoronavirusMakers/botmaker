#!/usr/bin/env python3

import json
import os
import re
import traceback
import telebot


class PersistDict(dict):
    def __init__(self, filename):
        self._filename = filename
        if os.path.exists(filename):
            d = json.load(open(filename))
            super().__init__(**d)

    def save(self):
        s = json.dumps(self, indent=1, sort_keys=True)
        open(self._filename+".bak", "w").write(open(self._filename).read())
        open(self._filename, "w").write(s)


settings = PersistDict("regional.json")
settings.save()


def format_user(user):
    msg = f"{user.first_name} {user.last_name}"
    msg += f" @{user.username}" if user.username else f" @{user.id}"
    return msg


def command_add_whitelist(bot, message, append=False, remove=False):
    to = message.chat.id if message.chat else message.from_user.id
    m = re.match(r"/(\w+)\s+(.*)", message.text.strip())
    if m:
        comando, usernames = m.groups()
        for username in usernames.split(" "):
            if append and username not in settings["whitelist"]:
                settings["whitelist"].append(username)
                settings.save()
                bot.send_message(to, f"Agregado @{username} correctamente!")
            if remove and username in settings["whitelist"]:
                settings["whitelist"] = [x for x in settings["whitelist"] if x != username]
                settings.save()
                bot.send_message(to, f"Borrado @{username} correctamente!")


def command_add_category_groupname(bot, message, append=False, remove=False):
    to = message.chat.id if message.chat else message.from_user.id
    m = re.match(r"/(\w+)\s+(\w+)\s+(.*)", message.text.strip())
    if m:
        comando, category, groupname = m.groups()
        reverse = {v: k for k, v in settings["chatlist"].items()}
        if groupname in reverse:
            if category not in settings["categories"]:
                settings["categories"][category] = []
                settings.save()
            groupid = reverse[groupname]
            if append and groupid not in settings["categories"][category]:
                settings["categories"][category].append(groupid)
                settings.save()
                bot.send_message(to, f"Agregado correctamente!")
            if remove and groupid in settings["categories"][category]:
                settings["categories"][category] = [x for x in settings["categories"][category] if x != groupid]
                settings.save()
                bot.send_message(to, f"Borrado correctamente!")
            if not settings["categories"][category]:
                del settings["categories"][category]
                settings.save()


def bot_command_control(bot, message):
    to = message.chat.id if message.chat else message.from_user.id
    text = message.text.strip()
    if text.endswith("@" + settings["bot_name"]):
        endlen = 1 + len(settings['bot_name'])
        text = text[:-endlen]
    if text == "/lista":
        msg = "Todos los grupos: "
        msg += ", ".join(sorted(chattitle for chatid, chattitle in settings["chatlist"].items()))
        bot.send_message(to, msg)
    elif text == "/admins":
        msg = "Todos los admins: "
        msg += ", ".join(sorted(usertitle for userid, usertitle in settings["admins"].items()))
        bot.send_message(to, msg)
    elif text == "/categories":
        msg = ""
        todos = set(settings["chatlist"].keys())
        for groupname, grouplist in settings["categories"].items():
            msg += f"Grupos de '{groupname}':\n"
            msg += ", ".join(settings["chatlist"].get(groupid, f"#{groupid}") for groupid in grouplist)
            msg += "\n\n"
            todos -= set(grouplist)
        if todos:
            msg += "Grupos sin categorizar:\n"
            msg += ", ".join(settings["chatlist"].get(groupid, f"#{groupid}") for groupid in todos)
        bot.send_message(to, msg)
    elif text.startswith("/addc"):
        command_add_category_groupname(bot, message, append=True)
    elif text.startswith("/delc"):
        command_add_category_groupname(bot, message, remove=True)
    elif text == "/whitelist":
        msg = ", ".join(f"@{username}" for username in settings["whitelist"])
        bot.send_message(to, msg)
    elif text.startswith("/addw"):
        command_add_whitelist(bot, message, append=True)
    elif text.startswith("/delw"):
        command_add_whitelist(bot, message, remove=True)
    elif text == "/help":
        msg = "Los comandos son:\n"
        msg += "  /lista: Para ver lista de canales\n"
        msg += "  /admins: Para ver lista de admins\n"
        msg += "  /categories: Para ver categorizacion\n"
        msg += "  /addc category groupname: Para agregar un grupo a una categoria\n"
        msg += "  /delc category groupname: Para borrar un grupo de una categoria\n"
        msg += "  /whitelist: Para ver usuarios con derecho a replica\n"
        msg += "  /addw username: Para permitir replicar a un usuario (sin @)\n"
        msg += "  /delw username: Para quitar permiso replica a un usuario (sin @)\n"
        msg += "  /help (Esta ayuda)"
        bot.send_message(to, msg)
    print(f"Amo {format_user(message.from_user)} textcut={text}")


def bot_command_broadcast(bot, message):
    text = message.text.strip() if message.text else ""
    if text == "broadcast":
        lista = settings["chatlist"].keys()
    elif text in settings["categories"].keys():
        lista = settings["categories"][text]
    else:
        return
    group_title = message.chat.title
    group_id = str(message.chat.id)
    reply = message.reply_to_message

    print(f"from {group_title} -> {text}. text={reply.text}")
    for igroup_id in lista:
        igroup_title = settings['chatlist'][igroup_id]
        bot.forward_message(igroup_id, group_id, reply.message_id)
        print(f"{text} -> {igroup_title}")
        bot.send_message(group_id, f"Reenviado a grupo {igroup_title}")


def bot_command_enter(bot, message):
    group_id = str(message.chat.id)
    if group_id not in settings['chatlist'] and group_id != settings["bot_groupid"]:
        group_title = message.chat.title
        print(f"Entro en grupo {group_title}")
        bot.send_message(settings["bot_groupid"], f"Me metieron en el grupo {group_title}")
        if group_id != settings["bot_groupid"]:
            settings['chatlist'][group_id] = group_title
            settings.save()


def bot_command_leave(bot, message):
    group_id = str(message.chat.id)
    group_title = message.chat.title
    print(f"Salgo de grupo {group_title}")
    bot.send_message(settings["bot_groupid"], f"Me sacaron del grupo {group_title}")
    if group_id in settings['chatlist']:
        del settings['chatlist'][group_id]
        settings.save()


def bot_command_all(bot, message):
    text = message.text.strip() if message.text else ""
    textcut = text[:10]
    if message.content_type == "new_chat_members":
        if message.new_chat_member.username == settings["bot_name"]:
            bot_command_enter(bot, message)
        else:
            print(f"Ignorando mensaje de {message.new_chat_member.username}")
    elif message.content_type == "left_chat_member":
        if message.left_chat_member.username == settings["bot_name"]:
            bot_command_leave(bot, message)
        else:
            print(f"Ignorando mensaje2 de {message.left_chat_member.username}")
    elif message.content_type == "text":
        group_title = message.chat.title
        group_id = str(message.chat.id)
        reply = message.reply_to_message
        if message.chat.type in ["group", "supergroup"]:  # mensaje desde grupo
            if group_id == settings["bot_groupid"]:  # grupo de admins
                if reply:
                    bot_command_broadcast(bot, message)
                else:
                    if message.from_user.id not in settings['admins']:
                        settings["admins"][str(message.from_user.id)] = message.from_user.username
                        settings.save()
                        print(f"agregando usuario {message.from_user.id} (@{message.from_user.username}) a admins")
                    bot_command_control(bot, message)
            else:
                bot_command_enter(bot, message)
                if reply and reply.from_user.username == settings["bot_name"]:
                    if message.from_user.username in settings["whitelist"]:
                        print(f"receiving {group_title} -> ADMIN. textcut={textcut}")
                        bot.reply_to(message, "Remitido al grupo de coordinación. Gracias!")
                        bot.send_message(settings["bot_groupid"], f"Nos dicen desde {group_title}...")
                        bot.forward_message(settings["bot_groupid"], group_id, message.message_id)
                    else:
                        bot.reply_to(message, "Por favor, contacte con un coordinador.")
                else:
                    print(f"ignorando2 {group_title}. textcut={textcut}")

        elif message.chat.type == "private":  # mensaje desde usuario
            if str(message.from_user.id) in settings['admins']:
                bot_command_control(bot, message)
            else:
                print(f"Ignorando3 {format_user(message.from_user)} textcut={textcut}")
        else:
            print(f"Nuevo tipo type={message.chat.type} textcut={textcut}")
    else:
        print(f"Mensaje desconocido {message}")


bot = telebot.TeleBot(settings["token"])


@bot.message_handler(content_types=["text", "new_chat_members", "left_chat_member"])
def command_all(message):
    try:
        return bot_command_all(bot, message)
    except Exception:
        print("Algo se ha roto :(")
        print(traceback.format_exc())


print("main loop polling...")
bot.polling()
