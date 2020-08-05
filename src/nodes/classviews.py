from django.views import generic
from . import models


class NodeListView(generic.ListView):
    model = models.Node

    def get_queryset(self):
        return super().get_queryset().filter(promoted=True)
        # return super().get_queryset().countries().with_uris()


class NodeSlugView(generic.DetailView):
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    model = models.Node


class MarkdownView(generic.ListView, generic.base.TemplateResponseMixin):
    model = models.Node
    template_name = "nodes/markdown.md"
    content_type = "text/plain"

    def get_queryset(self):
        return super().get_queryset().with_data
