from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth import login, logout # Make sure login and logout are imported
from .models import Acusinema, Event, SiteSettings, ContactMessage, SliderImage
from .forms import ContactForm, CustomUserCreationForm, CustomAuthenticationForm
from users.models import CustomUser
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required

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
    site_settings = SiteSettings.objects.first() # Renamed variable for clarity
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact')
    else:
        form = ContactForm()
    context = {
        'settings': site_settings, # Use the renamed variable
        'form': form,
    }
    return render(request, 'contact.html', context)

@login_required # Sadece giriş yapmış kullanıcılar erişebilir
def profile_page(request):
    """Kullanıcının profil bilgilerini gösterir."""
    user = request.user # Giriş yapmış kullanıcıyı al
    context = {
        'user_profile': user # Template'e göndermek için context'e ekle
    }
    return render(request, 'profile.html', context)

def account_page(request):
    # Redirect logged-in users away from login/register page (optional but good practice)
    # if request.user.is_authenticated:
    #     return redirect('homepage') # Or redirect to a profile page if you create one

    login_form = CustomAuthenticationForm()
    register_form = CustomUserCreationForm()
    active_tab = 'login' # Default tab to show

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                # Check if user account is active AND email is verified
                if user.is_active and user.is_email_verified:
                    login(request, user)
                    # Redirect to the page they came from or homepage
                    next_url = request.GET.get('next', 'homepage')
                    return redirect(next_url)
                elif not user.is_email_verified:
                     messages.error(request, 'Your email address is not verified. Please check your email for the verification code or request a new one.')
                     # Optionally, add logic here to resend verification email
                     return redirect('verify-email', user_id=user.pk) # Redirect to verification page
                else: # Account exists but is inactive for other reasons
                    messages.error(request, 'Your account is currently inactive. Please contact support.')
                    active_tab = 'login' # Keep login tab active to show error
            else:
                # Form is invalid, stay on login tab to show errors
                active_tab = 'login'

        elif 'register_submit' in request.POST:
            submitted_email = request.POST.get('email')
            # Check if an unverified user with this email exists and delete it before creating a new one
            if submitted_email:
                try:
                    existing_unverified_user = CustomUser.objects.get(
                        email=submitted_email,
                        is_active=False,
                        is_email_verified=False
                    )
                    existing_unverified_user.delete()
                    print(f"Deleted old unverified record for: {submitted_email}")
                except CustomUser.DoesNotExist:
                    pass # No old record found, proceed normally

            register_form = CustomUserCreationForm(request.POST)
            active_tab = 'register' # Keep register tab active

            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.is_active = False # Keep inactive until verified
                user.save()

                user.generate_verification_code() # Generate and save the code

                # Build verification URL for the email
                verification_url = request.build_absolute_uri(
                    reverse('verify-email', kwargs={'user_id': user.pk})
                )

                # Prepare email content
                subject = 'Acusinema Account Verification'
                message_body = ( # Renamed variable for clarity
                    f'Hello {user.first_name},\n\n'
                    f'Please use the following code to verify your Acusinema account:\n\n'
                    f'Your Verification Code: {user.verification_code}\n\n'
                    f'You can enter the code by clicking this link: {verification_url}\n\n'
                    'Thanks,\nThe Acusinema Team'
                )

                # Send the verification email using settings.py configuration
                try:
                    send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [user.email])
                    messages.success(request, 'Account created! Please check your email for the verification code to activate your account.')
                    return redirect('verify-email', user_id=user.pk) # Redirect to verification page
                except Exception as e:
                    messages.error(request, f'Could not send verification email. Please try again later or contact support. Error: {e}')
                    # Optional: Clean up the created user if email fails
                    # user.delete()
                    active_tab = 'register' # Stay on register tab
            # else: Form is invalid, errors will be shown automatically

    # Prepare context for rendering the template
    context = {
        'login_form': login_form,
        'register_form': register_form,
        'active_tab': active_tab # Helps template show the correct form tab
    }
    return render(request, 'account.html', context)


def verify_email(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)

    # Prevent already verified users from accessing this page directly
    if user.is_active and user.is_email_verified:
        messages.info(request, 'Your account is already verified.')
        return redirect('homepage')

    if request.method == 'POST':
        code = request.POST.get('verification_code', '').strip() # Get code and remove whitespace
        if code and code == user.verification_code:
            user.is_active = True
            user.is_email_verified = True
            user.verification_code = None # Clear the code after successful verification
            user.save()
            login(request, user) # Log the user in automatically
            messages.success(request, 'Your email address has been successfully verified. Welcome!')
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid verification code. Please try again.')

    # For GET request or if POST fails
    return render(request, 'verify_email.html', {'user': user})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.") # Optional: Add a success message
    return redirect('homepage')