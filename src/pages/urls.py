from django.conf.urls import url
from . import classviews

urlpatterns = [
    url(r'^$', classviews.PageListView.as_view(), name='page_list'),
    url(r'^(?P<slug>[//\w-]+)$', classviews.PageSlugView.as_view(), name='page_slug'),
]
