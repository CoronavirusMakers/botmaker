from django.core.management.base import BaseCommand  # , CommandError
import pycountry
from geolinks.models import Place, Subdivision


def get_create_subdivision(name):
    sd, created = Subdivision.objects.get_or_create(name=name)
    return sd


def get_create_place(placedata):
    if placedata.parent:
        parent = get_create_place(placedata.parent)
    else:
        parent = Place.objects.get(slug=placedata.country.alpha_2)
    defaults = {'name': placedata.name, 'parent': parent, 'subdivision_id': get_create_subdivision(placedata.type).id}
    p, created = Place.objects.get_or_create(slug=placedata.code, defaults=defaults)
    return p


class Command(BaseCommand):
    help = "Importa los datos de pycountry"

    def handle(self, *app_labels, **options):

        for country in pycountry.countries:
            defaults = {'name': country.name, 'subdivision': get_create_subdivision('Country')}
            c, created = Place.objects.get_or_create(slug=country.alpha_2, defaults=defaults)

        for placedata in pycountry.subdivisions:
            print(placedata)
            get_create_place(placedata)
