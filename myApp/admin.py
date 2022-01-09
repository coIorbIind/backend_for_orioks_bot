from django.contrib import admin
from . models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_username', 'user')
    list_display_links = ('id', 'telegram_username')
    search_fields = ('telegram_username', )
