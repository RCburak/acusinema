# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from .models import Acusinema, Event, SiteSettings, ContactMessage, SliderImage
from .forms import ContactForm, CustomUserCreationForm, CustomAuthenticationForm
from users.models import CustomUser 
from django.core.mail import send_mail
from django.urls import reverse

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
    login_form = CustomAuthenticationForm()
    register_form = CustomUserCreationForm()
    
    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                # Sadece e-postası doğrulanmış ve aktif kullanıcılar giriş yapabilsin
                if user.is_active and user.is_email_verified:
                    login(request, user)
                    return redirect('homepage')
                else:
                    messages.error(request, 'Hesabınız aktif değil veya e-posta adresiniz doğrulanmamış. Lütfen e-postanıza gelen doğrulama kodunu girin.')
                    # Kullanıcıyı doğrulama sayfasına yönlendir
                    return redirect('verify-email', user_id=user.pk)

        elif 'register_submit' in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                # Kullanıcıyı kaydet ama henüz aktif etme
                user.is_active = False 
                user.save()

                # Doğrulama kodu oluştur ve kaydet
                user.generate_verification_code()

                # Doğrulama e-postası gönder
                verification_url = request.build_absolute_uri(
                    reverse('verify-email', kwargs={'user_id': user.pk})
                )
                
                subject = 'Acusinema Hesap Doğrulama'
                message = (
                    f'Merhaba {user.first_name},\n\n'
                    f'Hesabınızı doğrulamak için lütfen aşağıdaki kodu kullanın:\n\n'
                    f'Doğrulama Kodunuz: {user.verification_code}\n\n'
                    f'Kodu girmek için bu linke tıklayabilirsiniz: {verification_url}\n\n'
                    'Teşekkürler,\nAcusinema Ekibi'
                )
                
                send_mail(subject, message, 'noreply@acusinema.com', [user.email])
                
                messages.success(request, 'Hesabınız oluşturuldu! Lütfen e-posta adresinize gönderilen doğrulama kodunu girerek hesabınızı aktive edin.')
                return redirect('verify-email', user_id=user.pk)
    
    context = {
        'login_form': login_form,
        'register_form': register_form
    }
    return render(request, 'account.html', context)

def verify_email(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        code = request.POST.get('verification_code')
        if code == user.verification_code:
            user.is_active = True
            user.is_email_verified = True
            user.save()
            login(request, user)
            messages.success(request, 'E-posta adresiniz başarıyla doğrulandı. Hoş geldiniz!')
            return redirect('homepage')
        else:
            messages.error(request, 'Geçersiz doğrulama kodu.')
    return render(request, 'verify_email.html', {'user': user})

def logout_view(request):
    logout(request)
    return redirect('homepage')