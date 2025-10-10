# core/views.py

from django.shortcuts import render
from .models import Event, Acusinema # Acusinema'yı import etmeyi unutmayın
from django.utils import timezone
from django.core.paginator import Paginator

def anasayfa(request):
    context = {
        'baslik': 'AcuSinema Kulübü',
        'karsilama_metni': 'Sinema tutkunlarının buluşma noktası.'
    }
    return render(request, 'anasayfa.html', context)

def iletisim_sayfasi(request):
    return render(request, 'iletisim.html')

def filmler_sayfasi(request):
    # URL'den 'q' adında bir arama parametresi gelip gelmediğini kontrol et
    query = request.GET.get('q')
    
    # Başlangıçta tüm filmleri al
    film_listesi = Acusinema.objects.all()
    
    # Eğer bir arama sorgusu varsa, film listesini başlığa göre filtrele
    if query:
        # __icontains: büyük/küçük harf duyarsız arama yapar
        film_listesi = film_listesi.filter(title__icontains=query)
    
    # Paginator nesnesi oluşturuyoruz: Her sayfada 6 film olacak
    paginator = Paginator(film_listesi, 6)
    
    # URL'den gelen sayfa numarasını alıyoruz
    sayfa_numarasi = request.GET.get('page')
    
    # İlgili sayfadaki filmleri alıyoruz
    sayfadaki_filmler = paginator.get_page(sayfa_numarasi)
    
    context = {
        'movies': sayfadaki_filmler,
        'search_query': query, # Arama sorgusunu template'e geri gönderiyoruz
    } 
    return render(request, 'filmler.html', context)

def etkinlikler_sayfasi(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(event_date__gte=now).order_by('event_date')
    past_events = Event.objects.filter(event_date__lt=now).order_by('-event_date')
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'etkinlikler.html', context)