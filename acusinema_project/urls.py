# acusinema_project/urls.py

from django.contrib import admin
from django.urls import path
from core.views import anasayfa, iletisim_sayfasi, filmler_sayfasi, etkinlikler_sayfasi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', anasayfa, name='anasayfa'),
    path('iletisim/', iletisim_sayfasi, name='iletisim'),
    path('filmler/', filmler_sayfasi, name='filmler'),
    path('etkinlikler/', etkinlikler_sayfasi, name='etkinlikler'),
]