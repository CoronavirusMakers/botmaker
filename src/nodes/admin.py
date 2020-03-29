from django.contrib import admin
from . import models


@admin.register(models.Node)
class NodeAdmin(admin.ModelAdmin):
    autocomplete_fields = ('parent', )
    search_fields = ('slug', 'title', 'text')
    list_filter = ('promoted', )
    list_display = ('slug', 'title', 'summary', 'promoted')
    readonly_fields = ('uris', )


@admin.register(models.Subdivision)
class SubdivisionAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    list_display = ('title', )


@admin.register(models.Uri)
class UriAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'summary', 'node')
    autocomplete_fields = ('node', )
    search_fields = ('title', 'url', 'text')
    save_on_top = True
