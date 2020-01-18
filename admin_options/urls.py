from django.urls import path
from .views import (
    admin_home, AdminContactListView, AdminContactDetailView, AdminContactCreateView, LoggedInUserListView
)


urlpatterns = [
    path('', admin_home, name='admin-home'),
    path('add/', AdminContactCreateView.as_view(), name='admin-contacts-add'),
    path('view/', AdminContactListView.as_view(), name='admin-contacts-browse'),
    path('view/logged-in-users/', LoggedInUserListView.as_view(), name='admin-loggedinuser'),
    path('view/user-access-review/', LoggedInUserListView.as_view(), name='admin-useraccessreview'),
    path('view/<slug:slug>/', AdminContactDetailView.as_view(), name='admin-contacts-view'),
]