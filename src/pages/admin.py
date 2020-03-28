from django.contrib import admin
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'summary', 'is_web')
    list_filter = ('is_web', )
