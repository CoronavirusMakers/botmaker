from django.views import generic
from . import models


class PageListView(generic.ListView):
    model = models.Page


class PageSlugView(generic.DetailView):
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    model = models.Page
