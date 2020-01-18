from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Path to include Admin page
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('phonebook-manager/', admin.site.urls, name='manage'),
    path('admin-options/', include('admin_options.urls')),
    # Path to include users app
    path('', include('users.urls')),
    # Path to include contacts app
    path('contacts/', include('contacts.urls')),
    # Path to include Django-Allauth urls
    path('accounts/', include('allauth.urls')),
    # Path to include Django Rest Framework API endpoints
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
