from django.core.management.base import BaseCommand  # , CommandError
import pycountry
from geolinks.models import Place


def get_crea_place(place):
    if place.parent:
        parent = get_crea_place(place.parent)
    else:
        parent = Place.objects.get(slug=place.country.alpha_2)
    p, created = Place.objects.get_or_create(slug=place.code, defaults={'name': place.name, 'parent': parent})
    return p


class Command(BaseCommand):
    help = "Importa los datos de pycountry"

    def handle(self, *app_labels, **options):

        for country in pycountry.countries:
            c, created = Place.objects.get_or_create(slug=country.alpha_2, defaults={'name': country.name})

        for place in pycountry.subdivisions:
            get_crea_place(place)
