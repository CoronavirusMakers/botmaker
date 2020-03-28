from django.db import models


class Page(models.Model):
    slug = models.CharField(max_length=255, unique=True, help_text="Escribe /start para el mensaje de bienvenida")
    text = models.TextField()
    is_web = models.BooleanField(default=False, help_text="Si se muestra en portada en la web")

    @property
    def summary(self, n=60):
        if len(self.text) > n:
            return self.text[:n] + "..."
        else:
            return self.text

    def __str__(self):
        return "{}: {}...".format(self.slug, self.summary)
