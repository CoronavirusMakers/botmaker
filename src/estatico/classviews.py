from django.views.generic import TemplateView


class EstaticoView(TemplateView):
    template_name = "estatico/index.html"


class EstaticoSlugView(TemplateView):
    template_name = "estatico/slug.html"
