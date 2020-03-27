from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from location_field.models.plain import PlainLocationField


class PlaceQuerySet(models.QuerySet):
    def countries(self):
        return self.filter(parent__isnull=True)

    def with_uris(self):
        return self.filter(uris__gt=0)


class Subdivision(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Place(models.Model):
    slug = models.SlugField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE)
    parent = models.ForeignKey('geolinks.Place', on_delete=models.CASCADE, blank=True, null=True)
    uris = models.IntegerField(default=0)

    objects = PlaceQuerySet.as_manager()

    @property
    def slugq(self):
        return self.slug.replace("_", "\\_")

    def content(self):
        return render_to_string("geolinks/place_detail.md", {'object': self})

    @staticmethod
    def all_content():
        return render_to_string("geolinks/place_list.md", {'object_list': Place.objects.countries().with_uris()})

    def update_uris(self):
        self.uris = self.uri_set.count() + sum(Place.objects.filter(parent=self).values_list('uris', flat=True))
        self.save()
        if self.parent:
            self.parent.update_uris()

    def parents(self):
        if self.parent:
            return self.parent.parents() + [self.parent]
        else:
            return []

    def __str__(self):
        return "{} ({})".format(self.name, self.slug)

    class Meta:
        ordering = ('subdivision', 'name', )
        verbose_name = "lugar"
        verbose_name_plural = "lugares"


class Uri(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    location = PlainLocationField(based_fields=['place'], zoom=7, blank=True, null=True)
    permanent = models.BooleanField(default=False, help_text="Iniciativa permanente o solo para el coronavirus")
    validated = models.BooleanField(default=False, help_text="Al validarse se hace visible")

    @property
    def summary(self, n=60):
        if not self.description:
            return "-"
        elif len(self.description) > n:
            return self.description[:n] + "..."
        else:
            return self.description

    def __str__(self):
        return "{} ({})".format(self.title, self.place)


@receiver(post_save, sender=Uri)
def postsave_uri(sender, instance, raw, *args, **kwargs):
    if not raw:
        instance.place.update_uris()
