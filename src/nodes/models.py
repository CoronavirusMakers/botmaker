from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse
from location_field.models.plain import PlainLocationField


class NodeQuerySet(models.QuerySet):
    def top(self):
        return self.filter(parent__isnull=True)

    def with_data(self):
        return self.filter(Q(uris__gt=0) | Q(text__isnull=False))


class Subdivision(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = "subdivisión"
        verbose_name_plural = "subdivisiones"


class Node(models.Model):
    slug = models.SlugField(max_length=20, unique=True, help_text="Esto son los comandos del bot, pero sin la '/' inicial")
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True, help_text="Es lenguaje markdown. Cuidado al escribir '_' y '*': Escápalos con '\_' y '\*'. Y despues de guardar, comprueba que se ven bien tanto el bot como la web.")
    promoted = models.BooleanField(default=False, help_text="Si se muestra en portada en la web")
    subdivision = models.ForeignKey(Subdivision, on_delete=models.SET_NULL, blank=True, null=True)
    parent = models.ForeignKey(
        'nodes.Node',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    uris = models.IntegerField(default=0)

    objects = NodeQuerySet.as_manager()

    @property
    def summary(self, n=60):
        if not self.text:
            return ""
        elif len(self.text) > n:
            return self.text[:n] + "..."
        else:
            return self.text

    def content(self):
        return render_to_string("nodes/node_detail.md", {'object': self})

    def update_uris(self):
        self.uris = self.uri_set.count() + sum(
            Node.objects.filter(parent=self).values_list('uris', flat=True))
        self.save()
        if self.parent:
            self.parent.update_uris()

    def parents(self):
        if self.parent:
            return self.parent.parents() + [self.parent]
        return []

    def get_absolute_url(self):
        return reverse('node_slug', args=[self.slug])

    def __str__(self):
        return "{} (/{})".format(self.title, self.slug)

    class Meta:
        ordering = ('subdivision', 'title')
        verbose_name = "nodo"
        verbose_name_plural = "nodos"


class Uri(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    text = models.TextField(blank=True, null=True)
    location = PlainLocationField(
        based_fields=['node'],
        zoom=7,
        blank=True,
        null=True,
    )

    @property
    def summary(self, n=60):
        if not self.text:
            return ""
        elif len(self.text) > n:
            return self.text[:n] + "..."
        else:
            return self.text

    def get_absolute_url(self):
        return reverse('node_slug', args=[self.node.slug])

    def __str__(self):
        return "{} ({})".format(self.title, self.node)

    class Meta:
        ordering = ('title', )
        verbose_name = "enlace"
        verbose_name_plural = "enlaces"


@receiver(post_save, sender=Uri)
def postsave_uri(sender, instance, raw, *args, **kwargs):
    if not raw:
        instance.node.update_uris()
