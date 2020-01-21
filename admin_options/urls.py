from django.urls import path
from .views import (
    admin_home, AdminContactListView, AdminContactDetailView, AdminContactCreateView, LoggedInUserListView,
    RegisteredUsersListView, PendingUsersListView, UserAccessReviewListView, LoggedInUserDeleteView
)


urlpatterns = [
    path('', admin_home, name='admin-home'),
    path('add/', AdminContactCreateView.as_view(), name='admin-contacts-add'),
    path('view/', AdminContactListView.as_view(), name='admin-contacts-browse'),
    path('view/registered-users/', RegisteredUsersListView.as_view(), name='admin-registeredusers'),
    path('view/pending-users/', PendingUsersListView.as_view(), name='admin-pendingusers'),
    path('view/logged-in-users/', LoggedInUserListView.as_view(), name='admin-loggedinusers'),
    path('view/logged-in-users/<int:pk>/', LoggedInUserDeleteView.as_view(), name='admin-loggedinusers-logout'),
    path('view/user-access-review/', UserAccessReviewListView.as_view(), name='admin-useraccessreview'),
    path('view/<slug:slug>/', AdminContactDetailView.as_view(), name='admin-contacts-view'),
]