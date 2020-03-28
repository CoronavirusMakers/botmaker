from django.conf.urls import url
from . import classviews

urlpatterns = [
    url(r'^location/$', classviews.LocationsView.as_view(), name='geolinks_locations'),
    url(r'^location/(?P<slug>[\w-]+)/$', classviews.LocationView.as_view(), name='geolinks_location'),
    url(r'^$', classviews.CountriesView.as_view(), name='geolinks_countries'),
    url(r'^(?P<slug>[\w-]+)/$', classviews.PlaceView.as_view(), name='geolinks_place'),
]
