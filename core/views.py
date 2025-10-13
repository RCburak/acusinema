# core/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
# Gerekli formları ve fonksiyonları import ediyoruz
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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
            messages.success(request, 'Mesajınız başarıyla gönderildi.')
            return redirect('iletisim')
    else:
        form = ContactForm()

    context = {
        'settings': settings,
        'form': form,
    }
    return render(request, 'iletisim.html', context)

# --- YENİ HESAP (GİRİŞ/KAYIT) VIEW'İ ---
def hesap_sayfasi(request):
    login_form = AuthenticationForm()
    register_form = UserCreationForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('anasayfa')
        elif 'register_submit' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Hesabınız başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.')
                return redirect('hesap')

    context = {
        'login_form': login_form,
        'register_form': register_form
    }
    return render(request, 'hesap.html', context)

def cikis_yap(request):
    logout(request)
    return redirect('anasayfa')