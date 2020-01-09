from django.urls import path
from .views import (
    ContactListView, ContactCreateView, ContactDetailView, ContactUpdateView, ContactDeleteView, contacts_home,
    contacts_about
)


urlpatterns = [
    path('', contacts_home, name='contacts-home'),
    path('home/', contacts_home, name='contacts-home'),
    path('add/', ContactCreateView.as_view(), name='contacts-add'),
    path('view/', ContactListView.as_view(), name='contacts-browse'),
    path('view/<slug:slug>/', ContactDetailView.as_view(), name='contacts-view'),
    path('view/<slug:slug>/update/', ContactUpdateView.as_view(), name='contacts-update'),
    path('view/<slug:slug>/delete/', ContactDeleteView.as_view(), name='contacts-delete'),
    path('about/', contacts_about, name='contacts-about'),
]
