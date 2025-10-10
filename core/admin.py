# core/admin.py

from django.contrib import admin
from .models import Acusinema, Event

# ... (AcusinemaAdmin sınıfınız burada aynı kalıyor) ...
class AcusinemaAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'release_date')
    search_fields = ('title', 'director')
    list_filter = ('release_date', 'director')
    date_hierarchy = 'release_date'


# --- GÜNCELLENEN EVENT ADMIN SINIFI ---
class EventAdmin(admin.ModelAdmin):
    # Liste sayfasında slug'ı da gösterelim
    list_display = ('title', 'location', 'event_date', 'slug')
    list_filter = ('event_date', 'location')
    search_fields = ('title', 'location')

    # Ekleme/Düzenleme sayfasındaki alanları grupluyoruz
    fieldsets = (
        ('Etkinlik Detayları', {
            'fields': ('title', 'slug', 'description')
        }),
        ('Zaman ve Mekan', {
            'fields': ('event_date', 'location')
        }),
    )

    # 'slug' alanını 'title' alanından otomatik olarak doldur
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Acusinema, AcusinemaAdmin)
admin.site.register(Event, EventAdmin)