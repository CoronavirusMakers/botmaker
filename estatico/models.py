from django.db import models


class Pagina(models.Model):
    slug = models.CharField(max_length=255, unique=True, help_text="Escribe /start para el mensaje de bienvenida")
    texto = models.TextField()
    visitas = models.IntegerField(default=0)

    def __str__(self):
        return "{}: {}...".format(self.slug, self.texto[:10])
