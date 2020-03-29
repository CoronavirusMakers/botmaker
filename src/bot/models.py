from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
import string
import secrets  # python3.6


def generate_password(n=10):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(n))
    return password


class TelegramUser(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    ident = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_bot = models.BooleanField()
    language_code = models.CharField(max_length=255, blank=True, null=True)
    web_group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def reset_or_create_webuser_message(self):
        defaults_dict = {
            'first_name': self.first_name,
            'last_name': self.last_name or "-",
            'is_active': True,
        }
        if not self.web_group:
            return "Lo siento, para tener acceso a la web necesitas que un administrador te autorice"
        if not self.username:
            return "Lo siento, para tener acceso a la web necesitas tener un 'telegram nick'"
        u, created = User.objects.get_or_create(
            username=self.username,
            defaults=defaults_dict,
        )
        password = generate_password()
        u.set_password(password)
        u.is_staff = True
        u.save()
        if self.web_group not in u.groups.all():
            u.groups.add(self.web_group)
        u.save()
        # FIXME esto se podría pasar a templates/webuser.txt para poderlo maquetar al gusto
        return "Tienes acceso a {} con usuario '{}' y contraseña '{}'".format(
            settings.BASE_URL,
            u.username,
            password,
        )

    @staticmethod
    def get_or_update(defaults):
        defaults_dict = {
            'first_name': defaults.first_name,
            'username': defaults.username,
            'last_name': defaults.last_name,
            'is_bot': defaults.is_bot,
            'language_code': defaults.language_code,
        }
        t, created = TelegramUser.objects.get_or_create(
            ident=defaults.id,
            defaults=defaults_dict,
        )
        if not created:
            changed = False
            for key, value in defaults_dict.items():
                if getattr(t, key) != value:
                    print("Valor", key, "cambiado de", getattr(t, key), "a",
                          value)
                    setattr(t, key, value)
                    changed = True
            if changed:
                print("saving", t)
                t.save()
            else:
                pass  # print("not changed")
        return t

    @property
    def nick(self):
        if self.username:
            return "@" + self.username
        return "#" + str(self.ident)

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name or "",
                                   self.nick)
