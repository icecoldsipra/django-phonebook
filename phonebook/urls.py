from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import error_page

urlpatterns = [
    path('manage/', admin.site.urls, name='manage'),
    path('', include('users.urls')),
    path('contact/', include('contacts.urls')),
    path('error/', error_page, name='error-page')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
