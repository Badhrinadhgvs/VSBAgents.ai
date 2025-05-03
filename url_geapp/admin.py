from django.contrib import admin
from .models import DynamicPage

@admin.register(DynamicPage)
class DynamicPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'keywords')
    readonly_fields = ('slug', 'created_at')