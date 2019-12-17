from django.urls import path
from .views import (
    ContactCreateAPIView, ContactListAPIView, ContactRetrieveAPIView, ContactRetrieveUpdateAPIView,
    ContactDestroyAPIView, CustomUserRetrieveAPIView, CustomUserRetrieveUpdateAPIView
)


urlpatterns = [
    # users app API endpoints
    path('users/<int:pk>/', CustomUserRetrieveUpdateAPIView.as_view(), name='users-update-api'),
    # contacts app API endpoints
    path('add/', ContactCreateAPIView.as_view(), name='contacts-add-api'),
    path('view/', ContactListAPIView.as_view(), name='contacts-browse-api'),
    path('view/<int:pk>/', ContactRetrieveAPIView.as_view(), name='contacts-view-api'),
    path('view/<int:pk>/update/', ContactRetrieveUpdateAPIView.as_view(), name='contacts-update-api'),
    path('view/<int:pk>/delete/', ContactDestroyAPIView.as_view(), name='contacts-delete-api'),
]
