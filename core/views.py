# core/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm

# Modelleri ve formları tek bir yerden, temiz bir şekilde import ediyoruz
from .models import Acusinema, Event, SiteSettings, ContactMessage, SliderImage
from .forms import ContactForm


def anasayfa(request):
    vizyondaki_filmler = Acusinema.objects.order_by('-created_at')[:3]
    slider_resimleri = SliderImage.objects.filter(is_active=True).order_by('order')
    
    context = {
        'homepage_movies': vizyondaki_filmler,
        'slider_images': slider_resimleri,
    }
    return render(request, 'anasayfa.html', context)

def filmler_sayfasi(request):
    query = request.GET.get('q')
    film_listesi = Acusinema.objects.all()
    if query:
        film_listesi = film_listesi.filter(title__icontains=query)
    
    paginator = Paginator(film_listesi, 6)
    sayfa_numarasi = request.GET.get('page')
    sayfadaki_filmler = paginator.get_page(sayfa_numarasi)
    
    context = {
        'movies': sayfadaki_filmler,
        'search_query': query,
    } 
    return render(request, 'filmler.html', context)

def etkinlikler_sayfasi(request):
    now = timezone.now()
    
    # HATA BURADAYDI: .order_by('date') YANLIŞTI, 'event_date' OLARAK DÜZELTİLDİ
    upcoming_events = Event.objects.filter(event_date__gte=now).order_by('event_date')
    
    past_events = Event.objects.filter(event_date__lt=now).order_by('-event_date')
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'etkinlikler.html', context)

def iletisim_sayfasi(request):
    settings = SiteSettings.objects.first()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mesajınız başarıyla gönderildi. En kısa sürede size geri döneceğiz.')
            return redirect('iletisim')
    else:
        form = ContactForm()

    context = {
        'settings': settings,
        'form': form,
    }
    return render(request, 'iletisim.html', context)

def kayit_ol(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hesabınız oluşturuldu {username}! Giriş yapabilirsiniz.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/kayit_ol.html', {'form': form})