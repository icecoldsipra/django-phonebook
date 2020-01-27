from django.urls import path
from .views import (
    admin_home, AdminContactListView, AdminContactDetailView, AdminContactCreateView, LoggedInUserListView,
    RegisteredUsersListView, PendingUsersListView, UserAccessView, LoggedInUserDeleteView
)


urlpatterns = [
    path('', admin_home, name='admin-home'),
    path('contacts/add/', AdminContactCreateView.as_view(), name='admin-contacts-add'),
    path('contacts/view/', AdminContactListView.as_view(), name='admin-contacts-browse'),
    path('contacts/view/<slug:slug>/', AdminContactDetailView.as_view(), name='admin-contacts-view'),
    path('users/registered-users/', RegisteredUsersListView.as_view(), name='admin-registeredusers'),
    path('users/pending-users/', PendingUsersListView.as_view(), name='admin-pendingusers'),
    path('users/logged-in-users/', LoggedInUserListView.as_view(), name='admin-loggedinusers'),
    path('users/logged-in-users/<int:pk>/', LoggedInUserDeleteView.as_view(), name='admin-loggedinusers-logout'),
    path('users/user-access-review/', UserAccessView.as_view(), name='admin-useraccessview'),
]