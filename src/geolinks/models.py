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


class Base(models.Model):
    @property
    def slugq(self):
        return self.slug.replace("_", "\\_")

    def content(self):
        return render_to_string("geolinks/place_detail.md", {'object': self})

    @classmethod
    def all_content(klz):
        return render_to_string("geolinks/place_list.md", {'object_list': klz.objects.countries().with_uris()})

    def update_uris(self):
        self.uris = self.uri_set.count() + sum(type(self).objects.filter(parent=self).values_list('uris', flat=True))
        self.save()
        if self.parent:
            self.parent.update_uris()

    def parents(self):
        if self.parent:
            return self.parent.parents() + [self.parent]
        else:
            return []

    class Meta:
        abstract = True


class Location(Base):
    slug = models.SlugField(max_length=10, unique=True, blank=True, null=True)
    geonameid = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('geolinks.Location', on_delete=models.CASCADE, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    uris = models.IntegerField(default=0)

    objects = PlaceQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name = "localización"
        verbose_name_plural = "localizaciones"


class Place(Base):
    slug = models.SlugField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE)
    parent = models.ForeignKey('geolinks.Place', on_delete=models.CASCADE, blank=True, null=True)
    uris = models.IntegerField(default=0)

    objects = PlaceQuerySet.as_manager()

    def __str__(self):
        return "{} ({})".format(self.name, self.slug)

    class Meta:
        ordering = ('subdivision', 'name', )
        verbose_name = "lugar"
        verbose_name_plural = "lugares"


class Uri(models.Model):
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, blank=True, null=True)
    place2 = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    description = models.TextField(blank=True, null=True)
    location = PlainLocationField(based_fields=['place'], zoom=7, blank=True, null=True)

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
        instance.place2.update_uris()
