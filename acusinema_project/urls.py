# acusinema_project/urls.py

from django.contrib import admin
from django.urls import path
# 'anasayfa'ya ek olarak 'iletisim_sayfasi' view'ını da import ediyoruz
from core.views import anasayfa, iletisim_sayfasi 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', anasayfa, name='anasayfa'), # <-- Kök dizini anasayfaya bağla
    
    # YENİ EKLENEN PATH
    # /iletisim/ URL'sini iletisim_sayfasi view'ına bağlıyoruz
    path('iletisim/', iletisim_sayfasi, name='iletisim'),
]