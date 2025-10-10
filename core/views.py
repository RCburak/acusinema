# core/views.py

from django.shortcuts import render
from .models import Event  # Event modelini import ediyoruz
from django.utils import timezone # Zaman bilgisi için import ediyoruz

# --- Diğer view'leriniz ---
def anasayfa(request):
    context = {
        'baslik': 'AcuSinema Kulübü',
        'karsilama_metni': 'Sinema tutkunlarının buluşma noktası.'
    }
    return render(request, 'anasayfa.html', context)

def iletisim_sayfasi(request):
    return render(request, 'iletisim.html')

def filmler_sayfasi(request):
    context = {} 
    return render(request, 'filmler.html', context)

# --- GÜNCELLENEN ETKİNLİKLER VIEW'İ ---
def etkinlikler_sayfasi(request):
    now = timezone.now()
    
    # Gelecekteki etkinlikleri al ve en yakın tarihli olanı en üste koy
    upcoming_events = Event.objects.filter(event_date__gte=now).order_by('event_date')
    
    # Geçmiş etkinlikleri al ve en yeni olanı en üste koy
    past_events = Event.objects.filter(event_date__lt=now).order_by('-event_date')
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'etkinlikler.html', context)