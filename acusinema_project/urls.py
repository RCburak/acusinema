# acusinema_project/urls.py

from django.contrib import admin
from django.urls import path, reverse_lazy  # <-- reverse_lazy'yi EKLEYİN
from core import views as core_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # <-- BU SATIRI EKLEYİN

urlpatterns = [
    path('admin/', admin.site.urls),

    # Page URLs
    path('', core_views.homepage, name='homepage'),
    path('movies/', core_views.movies_page, name='movies'),
    path('events/', core_views.events_page, name='events'),
    path('contact/', core_views.contact_page, name='contact'),
    
    # User Action URLs
    path('account/', core_views.account_page, name='account'),
    path('logout/', core_views.logout_view, name='logout'),
    path('verify-email/<int:user_id>/', core_views.verify_email, name='verify-email'),

    # --- ŞİFRE SIFIRLAMA URL'LERİ (BURADAN İTİBAREN EKLEYİN) ---
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset_form.html', # Kullanılacak template
             email_template_name='password_reset_email.html', # Gönderilecek e-posta içeriği
             subject_template_name='password_reset_subject.txt', # Gönderilecek e-posta konusu
             success_url=reverse_lazy('password_reset_done') # Başarılı olursa yönlendir
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html' # "E-posta gönderildi" sayfası
         ),
         name='password_reset_done'),

    path('password-reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html', # Yeni şifre belirleme sayfası
             success_url=reverse_lazy('password_reset_complete') # Başarılı olursa yönlendir
         ),
         name='password_reset_confirm'),

    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html' # "Şifre değişti" sayfası
         ),
         name='password_reset_complete'),
    # --- ŞİFRE SIFIRLAMA URL'LERİ SONU ---
]

# To serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)