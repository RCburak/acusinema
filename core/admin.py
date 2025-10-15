from django.contrib import admin
from django.utils.html import format_html
from .models import Acusinema, Event, SiteSettings, ContactMessage, SliderImage

class AcusinemaAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'rating', 'created_at', 'display_poster')
    list_filter = ('genre', 'created_at')
    search_fields = ('title', 'genre')
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'poster')
        }),
        ('Detaylar', {
            'fields': ('genre', 'duration', 'rating')
        }),
    )
    
    readonly_fields = ('created_at',)

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

class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'email', 'created_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')

class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'display_image')
    list_editable = ('order', 'is_active') 

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "Resim Yok"
    display_image.short_description = 'Resim Önizleme'

admin.site.register(Acusinema, AcusinemaAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(SliderImage, SliderImageAdmin)