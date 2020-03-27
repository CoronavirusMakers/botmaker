from django.contrib import admin
from . import models


@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    autocomplete_fields = ('parent', )
    search_fields = ('slug', 'name')
    list_display = ('slug', 'name')


@admin.register(models.Uri)
class UriAdmin(admin.ModelAdmin):
    list_display = ('place', 'url')
    autocomplete_fields = ('place', )
