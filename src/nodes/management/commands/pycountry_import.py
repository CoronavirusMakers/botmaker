from django.core.management.base import BaseCommand  # , CommandError
import pycountry
from nodes.models import Node, Subdivision


def get_create_subdivision(title):
    sd, created = Subdivision.objects.get_or_create(title=title)
    return sd


def repair(s):
    return s.replace("-", "_")  # no funciona como /link_en telegram


def get_create_place(placedata):
    if placedata.parent:
        parent = get_create_place(placedata.parent)
    else:
        parent = Node.objects.get(slug=repair(placedata.country.alpha_2))
    defaults = {
        'title': placedata.name,
        'parent': parent,
        'subdivision_id': get_create_subdivision(placedata.type).id,
    }
    p, created = Node.objects.get_or_create(slug=repair(placedata.code), defaults=defaults)
    return p


class Command(BaseCommand):
    help = "Importa los datos de pycountry"

    def handle(self, *app_labels, **options):
        world, created = Node.objects.get_or_create(slug="world", defaults={'title': 'Mundo', 'promoted': True})

        for country in pycountry.countries:
            defaults = {'title': country.name, 'subdivision': get_create_subdivision('Country'), 'parent': world}
            c, created = Node.objects.get_or_create(slug=repair(country.alpha_2), defaults=defaults)

        for placedata in pycountry.subdivisions:
            get_create_place(placedata)
