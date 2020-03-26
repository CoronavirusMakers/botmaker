from django.conf.urls import url
from . import classviews

urlpatterns = [
    url(
        r'^$',
        classviews.EstaticoView.as_view(),
        name='estatico_view',
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        classviews.EstaticoSlugView.as_view(),
        name='estatico_slug_view',
    ),
]
