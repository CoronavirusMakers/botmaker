from django.conf.urls import url
from . import classviews

urlpatterns = [
    url(r'^$', classviews.NodeListView.as_view(), name='node_list'),
    url(r'^markdown$', classviews.MarkdownView.as_view(), name='markdown'),
    url(r'^(?P<slug>[//\w-]+)$', classviews.NodeSlugView.as_view(), name='node_slug'),
]
