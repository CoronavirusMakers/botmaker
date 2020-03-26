from django.contrib import admin
from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    list_display = ('ident', 'username', 'first_name', 'last_name', 'creation_date')
    readonly_fields = ('creation_date', )