from django.views import generic
from . import models


class CountriesView(generic.ListView):
    model = models.Place

    def get_queryset(self):
        return super().get_queryset().countries().with_uris()


class PlaceView(generic.DetailView):
    model = models.Place
