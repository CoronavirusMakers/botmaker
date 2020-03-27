from django.db import models


class Page(models.Model):
    slug = models.CharField(max_length=255, unique=True, help_text="Escribe /start para el mensaje de bienvenida")
    text = models.TextField()

    @property
    def summary(self, n=60):
        if len(self.text) > n:
            return self.text[:n] + "..."
        else:
            return self.text

    def __str__(self):
        return "{}: {}...".format(self.slug, self.summary)
