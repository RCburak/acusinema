# acusinema_project/urls.py

from django.contrib import admin
from django.urls import path, reverse_lazy # reverse_lazy is needed for success_url
from core import views as core_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views # Import Django's auth views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Page URLs
    path('', core_views.homepage, name='homepage'),
    path('movies/', core_views.movies_page, name='movies'),
    path('events/', core_views.events_page, name='events'),
    path('contact/', core_views.contact_page, name='contact'),

    # User Action URLs
    path('account/', core_views.account_page, name='account'), # Handles login & registration
    path('logout/', core_views.logout_view, name='logout'), # Handles logout
    path('verify-email/<int:user_id>/', core_views.verify_email, name='verify-email'), # Handles email verification

    # --- PASSWORD RESET URLs using Django's built-in views ---
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset_form.html', # Template for entering email
             email_template_name='password_reset_email.html', # Plain text email body
             subject_template_name='password_reset_subject.txt', # Email subject line
             success_url=reverse_lazy('password_reset_done') # Redirect after email is sent
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html' # Template showing "email sent" message
         ),
         name='password_reset_done'),

    path('password-reset/confirm/<uidb64>/<token>/', # URL sent in the email
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html', # Template for entering new password
             success_url=reverse_lazy('password_reset_complete') # Redirect after password is changed
         ),
         name='password_reset_confirm'),

    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html' # Template showing "password changed" message
         ),
         name='password_reset_complete'),
    # --- END PASSWORD RESET URLs ---
    path('profile/', core_views.profile_page, name='profile'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Serve static files locally too if needed