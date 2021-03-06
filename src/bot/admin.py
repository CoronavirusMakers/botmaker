from django.contrib import admin
from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    list_display = ('ident', 'username', 'first_name', 'last_name', 'creation_date', 'web_group', 'receive_unknown')
    readonly_fields = ('creation_date', 'ident', 'username', 'first_name', 'last_name', 'is_bot', 'language_code')
    list_filter = ('web_group', 'receive_unknown')
    search_fields = ('username', 'first_name', 'last_name')
