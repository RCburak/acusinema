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
            # Changed message to English
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact')
    else:
        form = ContactForm()
    context = {
        'settings': settings,
        'form': form,
    }
    return render(request, 'contact.html', context)

# Translate account_page messages and email content
def account_page(request):
    login_form = CustomAuthenticationForm()
    register_form = CustomUserCreationForm()
    active_tab = 'login'

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                if user.is_active and user.is_email_verified:
                    login(request, user)
                    return redirect('homepage')
                else:
                    # Changed message to English
                    messages.error(request, 'Your account is inactive or your email address is not verified. Please enter the verification code sent to your email.')
                    return redirect('verify-email', user_id=user.pk)
            else:
                active_tab = 'login'

        elif 'register_submit' in request.POST:
            submitted_email = request.POST.get('email')
            if submitted_email:
                try:
                    existing_unverified_user = CustomUser.objects.get(
                        email=submitted_email,
                        is_active=False,
                        is_email_verified=False
                    )
                    existing_unverified_user.delete()
                    print(f"Deleted old unverified record for: {submitted_email}") # Console message
                except CustomUser.DoesNotExist:
                    pass

            register_form = CustomUserCreationForm(request.POST)
            active_tab = 'register'

            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.is_active = False # Keep inactive until verified
                user.save()

                user.generate_verification_code()

                verification_url = request.build_absolute_uri(
                    reverse('verify-email', kwargs={'user_id': user.pk})
                )

                # Changed email subject and message to English
                subject = 'Acusinema Account Verification'
                message = (
                    f'Hello {user.first_name},\n\n'
                    f'Please use the following code to verify your account:\n\n'
                    f'Your Verification Code: {user.verification_code}\n\n'
                    f'You can click this link to enter the code: {verification_url}\n\n'
                    'Thanks,\nThe Acusinema Team'
                )

                send_mail(subject, message, 'noreply@acusinema.com', [user.email])

                # Changed message to English
                messages.success(request, 'Your account has been created! Please activate your account by entering the verification code sent to your email address.')
                return redirect('verify-email', user_id=user.pk)
            # else: Form is invalid, errors will be shown

    context = {
        'login_form': login_form,
        'register_form': register_form,
        'active_tab': active_tab
    }
    return render(request, 'account.html', context)


# Translate verify_email messages
def verify_email(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        code = request.POST.get('verification_code')
        if code == user.verification_code:
            user.is_active = True
            user.is_email_verified = True
            user.verification_code = None # Clear the code after successful verification
            user.save()
            login(request, user)
            # Changed messages to English
            messages.success(request, 'Your email address has been successfully verified. Welcome!')
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid verification code.')
    return render(request, 'verify_email.html', {'user': user})

# logout_view usually doesn't need translation, but double-check if you added messages
def logout_view(request):
    logout(request)
    # Optional: Add a success message
    # messages.success(request, "You have been logged out successfully.")
    return redirect('homepage')