from django.db import models


class TelegramUser(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    ident = models.IntegerField()
    first_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_bot = models.BooleanField()
    language_code = models.CharField(max_length=255, blank=True, null=True)

    @staticmethod
    def get_or_update(defaults):
        defaults_dict = {
            'ident': defaults.id,
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
                print("saving")
                t.save()
            else:
                print("not changed")
        return t

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, "@" + self.username or str(self.ident))
