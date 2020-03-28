from django.views import generic
from . import models


class PageListView(generic.ListView):
    model = models.Page

    def get_queryset(self):
        return super().get_queryset().filter(is_web=True)


class PageSlugView(generic.DetailView):
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    model = models.Page
