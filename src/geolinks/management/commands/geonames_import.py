from django.core.management.base import BaseCommand  # , CommandError
from geolinks.models import Location

"""
cd /tmp/
wget http://download.geonames.org/export/dump/allCountries.zip
wget http://download.geonames.org/export/dump/hierarchy.zip
apt-get install unzip
unzip allCountries.zip
unzip hierarchy.zip
egrep '(PCLI|ADM1|ADM2)' allCountries.txt > allCountries_lite.txt
"""


all_countries = set()


def get_countries(filename):
    countries = []
    for line in open(filename).readlines():
        geonameid, name, asciiname, alternatenames, latitude, longitude, \
            feature_class, feature_code, country_code, cc2, admin1_code, admin2_code, \
            admin3_code, admin4_code, population, elevation, dem, timezone, \
            modification_date = line.strip("\n").split("\t")
        # entries: up to ADM2: 44003 , up to ADM1: 4149
        if feature_code in ["PCLI", "ADM1"]:
            d = {"geonameid": geonameid, "latitude": latitude, "longitude": longitude, "name": name}
            if feature_code == "PCLI":
                d['slug'] = country_code
            countries.append(d)
            all_countries.add(geonameid)
    return countries


def get_parents(filename):
    parents = []
    for line in open(filename).readlines():
        parent, child, feature_code = line.strip("\n").split("\t")
        # print(parent, child, repr(feature_code))
        if feature_code == "ADM" and parent in all_countries and child in all_countries:
            parents.append((parent, child))
    return parents


def create_location(data):
    try:
        Location.objects.get_or_create(geonameid=data['geonameid'], defaults=data)
    except Exception as e:
        print(data, e)


def update_hierarchy(parentid, childid):
    try:
        parent = Location.objects.get(geonameid=parentid)
        child = Location.objects.get(geonameid=childid)
        child.parent = parent
        child.save()
    except Exception as e:
        print(parentid, childid, e)


class Command(BaseCommand):
    help = "Importa los datos de geonames"

    def handle(self, *app_labels, **options):
        for country in get_countries("/tmp/allCountries_lite.txt"):
            create_location(country)
        print("count=", len(all_countries))

        for parent, child in get_parents("/tmp/hierarchy.txt"):
            update_hierarchy(parent, child)
