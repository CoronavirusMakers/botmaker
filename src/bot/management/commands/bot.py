import telebot
from telebot import types

# import re

from django.core.management.base import BaseCommand  # , CommandError
from django.conf import settings
from bot.models import TelegramUser
from estatico.models import Pagina


# class TelegramStates:
#     def __init__(self):
#         self.states = {}
#
#     def set(self, key, **kwargs):
#         if key not in self.states:
#             self.states[key] = kwargs
#         else:
#             self.states[key].update(kwargs)
#
#     def get(self, key):
#         return self.states.get(key)
#
#     def clean(self, key):
#         if key in self.states:
#             del self.states[key]
#
#
# telegram_states = TelegramStates()
#
# #
# # Main functions
# #
#
#
# def _generic_tickets(user, what, **filter_args):
#     redmine = Redmine(settings.REDMINE_API_URL, key=settings.REDMINE_KEY, impersonate=user.login)
#     textos = []
#     for issue in redmine.issue.filter(**filter_args):
#         kwargs = dict(id=issue.id, project=issue.project, subject=issue.subject)
#         msg = "/ticket_{id} ({project}) {subject}".format(**kwargs)
#         textos.append(msg)
#     if len(textos) > 0:
#         msg = "Estos son los {}:\n".format(what) + "\n".join(textos)
#     else:
#         msg = "No tiene {}".format(what)
#     return msg
#
#
# def tickets_nobody_new(user):
#     return _generic_tickets(
#         user, "tickets nuevos sin coger",
#         assigned_to_id=USERS.NOBODY, status_id=STATUS.NEW)
#
#
# def tickets_nobody_in_progress(user):
#     return _generic_tickets(
#         user, "tickets en curso sin coger",
#         assigned_to_id=USERS.NOBODY, status_id=STATUS.IN_PROGRESS)
#
#
# def tickets_me_open(user):
#     return _generic_tickets(
#         user, "tickets abiertos cogidos por mi",
#         assigned_to_id=user.id, status_id=STATUS.OPEN)
#
#
# def tickets_open(user):
#     return _generic_tickets(
#         user, "tickets abiertos",
#         status_id=STATUS.OPEN)
#
#
# def tickets_in_progress(user):
#     return _generic_tickets(
#         user, "tickets en curso",
#         status_id=STATUS.IN_PROGRESS)
#
#
# def ticket_info(user, ticket_id):
#     redmine = Redmine(settings.REDMINE_API_URL, key=settings.REDMINE_KEY, impersonate=user.login)
#     try:
#         issue = redmine.issue.get(ticket_id)
#     except ResourceNotFoundError:
#         return "Ticket no se encuentra"
#     msg = "Ticket {}:\n".format(ticket_id)
#     msg += "- fecha: {}\n".format(issue.created_on)
#     msg += "- proyecto: {}\n".format(issue.project)
#     if issue.status.id != STATUS.CLOSED:
#         msg += "- estado: {} /cierra_{}\n".format(issue.status, ticket_id)
#     else:
#         msg += "- estado: {}\n".format(issue.status)
#     if issue.subject:
#         msg += "- asunto: {}\n".format(issue.subject)
#     if issue.description:
#         msg += "- descripción: {}\n".format(issue.description)
#     msg += "- url: {}issues/{}\n".format(settings.REDMINE_PUBLIC_URL, ticket_id)
#     try:
#         if issue.assigned_to.id == user.id:
#             msg += "- cogido por mi /suelta_{}\n".format(ticket_id)
#         else:
#             msg += "- cogido por: {} /coge_{}\n".format(issue.assigned_to, ticket_id)
#     except ResourceAttrError:
#         msg += "- sin coger /coge_{}\n".format(ticket_id)
#     for ij in issue.journals:
#         try:
#             msg += "- nota {}: {}\n".format(ij.id, ij.notes.strip())
#         except ResourceAttrError:
#             msg += "- nota {}: (error)\n".format(ij.id)
#     for te in issue.time_entries:
#         msg += "- entrada {}: {} ({:.2f}h)\n".format(te.id, te.comments.strip(), te.hours)
#     return msg.strip()
#
#
# def open_ticket(user, ticket_id):
#     redmine = Redmine(settings.REDMINE_API_URL, key=settings.REDMINE_KEY, impersonate=user.login)
#     try:
#         issue = redmine.issue.get(ticket_id)
#     except ResourceNotFoundError:
#         return "Ticket no se encuentra"
#     if issue.status.id == STATUS.NEW:
#         return "El /ticket_{} ya esta abierto!".format(ticket_id)
#     else:
#         redmine.issue.update(ticket_id, status_id=STATUS.NEW)
#         return "Acabas de abrir el /ticket_{}: {}".format(ticket_id, issue.subject)
#
#
# def ticket_assign(user, ticket_id):
#     redmine = Redmine(settings.REDMINE_API_URL, key=settings.REDMINE_KEY, impersonate=user.login)
#     try:
#         issue = redmine.issue.get(ticket_id)
#     except ResourceNotFoundError:
#         return "Ticket no se encuentra"
#     try:
#         if issue.assigned_to.id == user.id:
#             return "El /ticket_{} ya es tuyo!".format(ticket_id)
#     except ResourceAttrError:
#         pass  # sin coger
#     redmine.issue.update(ticket_id, assigned_to_id=user.id, status_id=STATUS.IN_PROGRESS)
#     return "Acabas de cogerte el /ticket_{}: {}".format(ticket_id, issue.subject)
#
#
# def ticket_forget(user, ticket_id):
#     redmine = Redmine(settings.REDMINE_API_URL, key=settings.REDMINE_KEY, impersonate=user.login)
#     try:
#         issue = redmine.issue.get(ticket_id)
#     except ResourceNotFoundError:
#         return "Ticket no se encuentra"
#     try:
#         if issue.assigned_to.id == 0:
#             return "El /ticket_{} ya esta suelto!".format(ticket_id)
#         elif issue.assigned_to.id == user.id:
#             redmine.issue.update(ticket_id, assigned_to_id=0)
#             return "Acabas de soltar el /ticket_{}: {}".format(ticket_id, issue.subject)
#         else:
#             return "El /ticket_{} no es tuyo!".format(ticket_id)
#     except ResourceAttrError:
#         return "El /ticket_{} ya esta suelto!".format(ticket_id)
#
#
# def ticket_close(user, ticket_id):
#     redmine = Redmine(settings.REDMINE_API_URL, key=settings.REDMINE_KEY, impersonate=user.login)
#     try:
#         issue = redmine.issue.get(ticket_id)
#     except ResourceNotFoundError:
#         return "Ticket no se encuentra"
#     if issue.status.id == STATUS.CLOSED:
#         return "El /ticket_{} ya esta cerrado!".format(ticket_id)
#     else:
#         redmine.issue.update(ticket_id, status_id=STATUS.CLOSED)
#         return "Acabas de cerrar el /ticket_{}: {}".format(ticket_id, issue.subject)
#
#
# def command_error(user):
#     return "Unknown command"
#
#
# def ticket_note(user, ticket_id, mensaje):
#     redmine = Redmine(settings.REDMINE_API_URL, key=settings.REDMINE_KEY, impersonate=user.login)
#     try:
#         redmine.issue.update(ticket_id, notes=mensaje)
#     except ResourceNotFoundError:
#         return "Ticket no se encuentra"
#     return "Anotado en el /ticket_{}".format(ticket_id)
#
#
# def ticket_time_entry(user, ticket_id, mensaje, minutes):
#     if isinstance(minutes, str):
#         if minutes[-1] in "hH":
#             hours = float(minutes[:-1])
#         elif minutes[-1] in "mM":
#             hours = float(minutes[:-1])/60.
#         else:
#             hours = float(minutes)/60.
#     else:
#         hours = minutes/60.
#
#     redmine = Redmine(settings.REDMINE_API_URL, key=settings.REDMINE_KEY, impersonate=user.login)
#     redmine.time_entry.create(issue_id=ticket_id, hours=hours,
#                               activity_id=settings.DEFAULT_ACTIVITY, comments=mensaje)
#     return "Anotado que has trabajado {minutes} minutos en el /ticket_{i}.\n" \
#         "Si quieres /suelta_{i} o /cierra_{i} o sigue trabajando".format(
#             minutes=int(hours*60), i=ticket_id)
#
# #
# # Commands for each previous function
# #
#
# EXPRESIONES = (
#     (r'/+nuevos', tickets_nobody_new),
#     (r'/+abandonados', tickets_nobody_in_progress),
#     (r'/+mios', tickets_me_open),
#     (r'/+abiertos', tickets_open),
#     (r'/+encurso', tickets_in_progress),
#     (r'/+(ticket)?_?(?P<ticket_id>\d+)', ticket_info),
#     (r'/+abre_?(?P<ticket_id>\d+)', open_ticket),
#     (r'/+coge_?(?P<ticket_id>\d+)', ticket_assign),
#     (r'/+suelta_?(?P<ticket_id>\d+)', ticket_forget),
#     (r'/+cierra_?(?P<ticket_id>\d+)', ticket_close),
#     (r'/+(\w+)', command_error),
#     # commands probably without leading /
#     (r'/?(nota)?_?(?P<ticket_id>\d+) (?P<mensaje>.*) (?P<minutes>[\d.]+[hHmM]?)', ticket_time_entry),
#     (r'/?(nota)?_?(?P<ticket_id>\d+) (?P<mensaje>.*)', ticket_note),
# )
#
#
# #
# # Authorized telegram users from Redmine
# # (in redmine we have a custom field for user called "telegram" type integer
# # with the telegram id of each user)
# #
#
# def get_telegram_users():
#     "Fills dictionary from redmine with objects for each authorized user"
#
#     redmine = Redmine(settings.REDMINE_API_URL, key=settings.REDMINE_KEY)
#     # We search all users from redmine that have a telegram id and we build
#     # a list of objects with useful data
#     out = {}
#     for user in redmine.user.all():
#         for cf in user.custom_fields:
#             if cf.name == "telegram":
#                 chatid = int(cf.value or 0)
#                 if chatid > 0:
#                     out[chatid] = SimpleNamespace(
#                         name="{} {}".format(user.firstname, user.lastname),
#                         login=user.login,
#                         id=user.id,
#                     )
#                     break
#     return out
#
# TELEGRAM_USERS = get_telegram_users()
# print("Usuarios de telegram-redmine:")
# pprint(TELEGRAM_USERS)
#
#
# #
# # Decorator for authorization
# #
#
# def _only_authorized(f):
#     def func(message):
#         if message.from_user.username:
#             username = "@{}".format(message.from_user.username)
#         else:
#             username = "{} {}".format(message.from_user.first_name, message.from_user.last_name)
#         date = datetime.datetime.utcfromtimestamp(message.date)
#         print("[{}] {} (#{}) escribió '{}'".format(
#             date, username, message.from_user.id, message.text))
#
#         chatid = message.from_user.id
#         if chatid not in TELEGRAM_USERS:
#             bot.reply_to(message, "No te conozco {}".format(chatid))
#             return
#         f(message)
#     return func
#
#
# #
# # Bot commands
# #
#
# @bot.message_handler(commands=['start'])
# def command_start(message):
#     msg = "Esto es un bot para interactuar con el Redmine de {}\n".format(settings.COMPANY)
#     msg += "Pica en /help para tener mas información\n"
#     bot.reply_to(message, msg)
#
#
# @bot.message_handler(commands=['help', '/help'])
# @_only_authorized
# def command_help(message):
#     msg = "Los siguientes comandos estan disponibles:\n"
#     msg += "/nuevos tickets nuevos sin coger\n"
#     msg += "/abandonados tickets en curso sin coger\n"
#     msg += "/mios tickets abiertos cogidos por mi\n"
#     msg += "/abiertos tickets abiertos\n"
#     msg += "/encurso tickets en curso\n"
#     bot.reply_to(message, msg)
#
#
# @bot.message_handler(commands=['tickets'])
# @bot.message_handler(func=lambda message: True)  # Pilla todos los comandos
# @_only_authorized
# def command_all(message):
#     "catch-all command that calls simplified functions with argument 'user' and tokens"
#     chatid = message.from_user.id
#     txt = message.text.strip()
#     user = TELEGRAM_USERS[chatid]
#     msg = "No entiendo"
#     try:
#         for regex, func in EXPRESIONES:
#             m = re.fullmatch(regex, txt, re.DOTALL)
#             if m:
#                 d = m.groupdict()
#                 # arguments are: user and a dictionary with named items of the regexp
#                 msg = func(user, **d)
#                 if 'ticket_id' in d:
#                     telegram_states.set(chatid, date=message.date, **d)
#                 else:
#                     telegram_states.clean(chatid)
#                 break
#         else:
#             if message.chat.type == "private":
#                 old = telegram_states.get(chatid)
#                 if old and 'ticket_id' in old:
#                     minutes = (message.date - old['date'])//60
#                     msg = ticket_time_entry(user, old['ticket_id'], txt, minutes)
#                     telegram_states.set(chatid, date=message.date)
#     except ValidationError as e:
#         msg = str(e)
#
#     msg = msg.strip()
#     print("----------Se le respondio------\n{}\n-----------".format(msg))
#     if message.chat.type == "private":
#         bot.send_message(chatid, msg)
#     else:
#         bot.reply_to(message, msg)

def bot_command_all(bot, message):
    u = TelegramUser.get_or_update(message.from_user)
    if message.content_type == "location":
        print("location=", message.location.latitude, message.location.longitude)
    elif message.content_type == "contact":
        print("contact=", message.contact.phone_number)
    elif message.content_type == "text":
        comando = message.text.strip()
        try:
            p = Pagina.objects.get(slug=comando)
            msg = p.texto
        except Pagina.DoesNotExist:
            msg = "No entiendo el comando {}".format(comando)
        print("mensaje=", message.text.strip(), "reply=", msg)
        print("no envio nada")
        # bot.send_message(u.ident, msg)
    else:
        print("error")
    # bot.reply_to(message, msg)

    # Using the ReplyKeyboardMarkup class
    # It's constructor can take the following optional arguments:
    # - resize_keyboard: True/False (default False)
    # - one_time_keyboard: True/False (default False)
    # - selective: True/False (default False)
    # - row_width: integer (default 3)
    # row_width is used in combination with the add() function.
    # It defines how many buttons are fit on each row before continuing on the next row.
    if False:
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('si', request_location=True)
        itembtn2 = types.KeyboardButton('no', request_contact=True)
        itembtn3 = types.KeyboardButton('puede')
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(u.ident, "Choose one letter:", reply_markup=markup)


class Command(BaseCommand):
    help = "Importa un extracto de lineas de cajasiete"

    def handle(self, *app_labels, **options):

        # proveedor_str = options.get("proveedor")
        # raise CommandError("Ha de especificar un proveedor")

        bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)

        @bot.message_handler(func=lambda message: True, content_types=["text", "location", "contact"])
        def command_all(message):
            return bot_command_all(bot, message)

        print("main loop polling...")
        bot.polling()


#
# The workflow used is very simple.
#
# The tickets begin in NEW state and without asignee
# - If someone asignates himself, status changes to IN_PROGRESS with asignee
# - If someone leaves the ticket, status maintains to IN_PROGRESS without asignee
# - If someone closes the ticket, status changes to CLOSED
#


# To remember:
#
# issue attributes:
# ['attachments', 'author', 'changesets', 'children', 'created_on', 'description',
# 'done_ratio', 'id', 'journals', 'priority', 'project', 'relations', 'start_date',
# 'status', 'subject', 'time_entries', 'tracker', 'updated_on', 'watchers']
#
# user attributes:
# ['contacts', 'deals', 'groups', 'id', 'issues', 'memberships', 'name', 'time_entries']
#
# issue journals
# ['created_on', 'details', 'id', 'notes', 'user']
