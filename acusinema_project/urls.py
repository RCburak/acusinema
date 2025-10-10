# acusinema_project/urls.py

from django.contrib import admin
from django.urls import path
from core.views import anasayfa, iletisim_sayfasi, filmler_sayfasi, etkinlikler_sayfasi

# Gerekli importları ekliyoruz
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', anasayfa, name='anasayfa'),
    path('iletisim/', iletisim_sayfasi, name='iletisim'),
    path('filmler/', filmler_sayfasi, name='filmler'),
    path('etkinlikler/', etkinlikler_sayfasi, name='etkinlikler'),
]

# Medya dosyalarını sunmak için bu satırları ekliyoruz
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)