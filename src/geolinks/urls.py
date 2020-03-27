from django.conf.urls import url
from . import classviews

urlpatterns = [
    url(r'^$', classviews.CountriesView.as_view(), name='geolinks_countries'),
    url(r'^(?P<slug>[\w-]+)/$', classviews.PlaceView.as_view(), name='geolinks_place'),
]
