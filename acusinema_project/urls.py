# acusinema_project/urls.py

from django.contrib import admin
from django.urls import path
from core.views import anasayfa # <-- core uygulamasından anasayfayı import et

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', anasayfa, name='anasayfa'), # <-- Kök dizini anasayfaya bağla
]