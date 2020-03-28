from django.contrib import admin
from . import models


@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    autocomplete_fields = ('parent', )
    search_fields = ('slug', 'name')
    list_display = ('slug', 'name')


@admin.register(models.Subdivision)
class SubdivisionAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', )


@admin.register(models.Uri)
class UriAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'summary', 'place')
    autocomplete_fields = ('place', )
