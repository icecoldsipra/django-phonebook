from django.urls import path
from .views import (
    ContactCreateAPIView, ContactListAPIView, ContactRetrieveAPIView, ContactRetrieveUpdateAPIView,
    ContactRetrieveDestroyAPIView, CustomUserRetrieveUpdateAPIView, CustomUserCreateAPIView
)


urlpatterns = [
    # users app API endpoints
    # path('register/', CustomUserCreateAPIView.as_view(), name='users-register-api'),
    path('users/<int:pk>/', CustomUserRetrieveUpdateAPIView.as_view(), name='users-update-api'),
    # contacts app API endpoints
    path('contacts/add/', ContactCreateAPIView.as_view(), name='contacts-add-api'),
    path('contacts/view/', ContactListAPIView.as_view(), name='contacts-browse-api'),
    path('contacts/view/<int:pk>/', ContactRetrieveAPIView.as_view(), name='contacts-view-api'),
    path('contacts/view/<int:pk>/update/', ContactRetrieveUpdateAPIView.as_view(), name='contacts-update-api'),
    path('contacts/view/<int:pk>/delete/', ContactRetrieveDestroyAPIView.as_view(), name='contacts-delete-api'),
]
