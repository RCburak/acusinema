# acusinema_project/urls.py

from django.contrib import admin
from django.urls import path
from core import views as core_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Sayfa URL'leri
    path('', core_views.anasayfa, name='anasayfa'),
    path('filmler/', core_views.filmler_sayfasi, name='filmler'),
    path('etkinlikler/', core_views.etkinlikler_sayfasi, name='etkinlikler'),
    path('iletisim/', core_views.iletisim_sayfasi, name='iletisim'),
    
    # Kullanıcı İşlem URL'leri
    path('hesap/', core_views.hesap_sayfasi, name='hesap'),
    path('cikis/', core_views.cikis_yap, name='logout'),
]

# Medya dosyalarını sunmak için
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)