# acusinema_project/urls.py

from django.contrib import admin
from django.urls import path
from core import views as core_views

from django.conf import settings
from django.conf.urls.static import static

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
]

# To serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)