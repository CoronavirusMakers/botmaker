from django.contrib import admin
from .models import Pagina


@admin.register(Pagina)
class PaginaAdmin(admin.ModelAdmin):
    list_display = ('slug', 'texto', 'visitas')
