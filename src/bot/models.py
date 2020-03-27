from django.db import models
from django.contrib.auth.models import User
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
    web_enabled = models.BooleanField(default=False)

    def reset_or_create_webuser_message(self):
        defaults_dict = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': True,
        }
        if not self.web_enabled or not self.username:
            return "Lo siento, no tienes acceso a la web."
        u, created = User.objects.get_or_create(username=self.username, defaults=defaults_dict)
        password = generate_password()
        u.set_password(password)
        u.save()
        # FIXME esto se podría pasar a templates/webuser.txt para poderlo maquetar al gusto
        return "Tienes acceso a {} con usuario '{}' y contraseña '{}'".format(settings.BASE_URL,
                                                                              u.username, password)

    @staticmethod
    def get_or_update(defaults):
        defaults_dict = {
            'first_name': defaults.first_name,
            'username': defaults.username,
            'last_name': defaults.last_name,
            'is_bot': defaults.is_bot,
            'language_code': defaults.language_code,
        }
        t, created = TelegramUser.objects.get_or_create(ident=defaults.id, defaults=defaults_dict)
        if not created:
            changed = False
            for key, value in defaults_dict.items():
                if getattr(t, key) != value:
                    print("Valor", key, "cambiado de", getattr(t, key), "a", value)
                    setattr(t, key, value)
                    changed = True
            if changed:
                print("saving", t)
                t.save()
            else:
                pass  # print("not changed")
        return t

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name or "", "@" + self.username or str(self.ident))
