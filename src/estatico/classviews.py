from django.views import generic
from . import models


class EstaticoView(generic.list.ListView):
    model = models.Pagina
    template_name = "estatico/index.html"


class EstaticoSlugView(generic.DetailView):
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    model = models.Pagina
    template_name = "estatico/slug.html"
