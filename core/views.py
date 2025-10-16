# core/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Acusinema, Event, SiteSettings, ContactMessage, SliderImage
from .forms import ContactForm
from .forms import ContactForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import Acusinema, Event, SiteSettings, ContactMessage, SliderImage


def homepage(request):
    movies_on_homepage = Acusinema.objects.order_by('-created_at')[:3]
    slider_images = SliderImage.objects.filter(is_active=True).order_by('order')
    context = {
        'homepage_movies': movies_on_homepage,
        'slider_images': slider_images,
    }
    return render(request, 'homepage.html', context)

def movies_page(request):
    query = request.GET.get('q')
    movie_list = Acusinema.objects.all()
    if query:
        movie_list = movie_list.filter(title__icontains=query)
    paginator = Paginator(movie_list, 6)
    page_number = request.GET.get('page')
    movies_on_page = paginator.get_page(page_number)
    context = {
        'movies': movies_on_page,
        'search_query': query,
    }
    return render(request, 'movies.html', context)

def events_page(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(event_date__gte=now).order_by('event_date')
    past_events = Event.objects.filter(event_date__lt=now).order_by('-event_date')
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'events.html', context)

def contact_page(request):
    settings = SiteSettings.objects.first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact')
    else:
        form = ContactForm()
    context = {
        'settings': settings,
        'form': form,
    }
    return render(request, 'contact.html', context)

def account_page(request):
    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('homepage')
        elif 'register_submit' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Your account has been created successfully! You can now log in.')
                return redirect('account')
    context = {
        'login_form': login_form,
        'register_form': register_form
    }
    return render(request, 'account.html', context)

def account_page(request):
    # Formları kendi custom formlarınızla değiştirin
    login_form = CustomAuthenticationForm()
    register_form = CustomUserCreationForm()
    
    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('homepage')
        elif 'register_submit' in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                # Kayıt sonrası otomatik giriş yaptırmak isterseniz aşağıdaki satırı ekleyebilirsiniz
                # login(request, user)
                messages.success(request, 'Hesabınız başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.')
                return redirect('account')
    
    context = {
        'login_form': login_form,
        'register_form': register_form
    }
    return render(request, 'account.html', context)


def logout_view(request):
    logout(request)
    return redirect('homepage')
