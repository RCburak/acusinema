# core/admin.py

from django.contrib import admin
from .models import Acusinema, Event
from django.utils.html import format_html

class AcusinemaAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'rating', 'duration', 'display_poster')
    list_filter = ('genre',)
    search_fields = ('title',)
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'poster')
        }),
        ('Detaylar', {
            'fields': ('genre', 'duration', 'rating')
        }),
    )

    def display_poster(self, obj):
        if obj.poster:
            return format_html('<img src="{}" width="50" style="border-radius: 5px;" />', obj.poster.url)
        return "Afiş Yok"
    display_poster.short_description = 'Afiş'

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'event_date', 'slug')
    list_filter = ('event_date', 'location')
    search_fields = ('title', 'location')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Acusinema, AcusinemaAdmin)
admin.site.register(Event, EventAdmin)