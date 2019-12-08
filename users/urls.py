from django.contrib.auth import views as auth_views
from django.urls import path
from.views import (
    UserLoginView,
    UserRegisterView,
    UserUpdateView,
    UserPasswordChangeView,
    UserPasswordResetView,
    UserPasswordResetDoneView,
    UserPasswordResetConfirmView,
    UserPasswordResetCompleteView,
    users_activate
)


urlpatterns = [
    path('', UserLoginView.as_view(), name='users-login'),
    path('login/', UserLoginView.as_view(), name='users-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/users_logout.html'), name='users-logout'),
    path('register/', UserRegisterView.as_view(), name='users-register'),
    path('profile/<int:pk>/', UserUpdateView.as_view(), name='users-profile'),
    path('activate/<uidb64>/<token>/', users_activate, name='users-activate'),
    path('password/change', UserPasswordChangeView.as_view(), name='password-change'),
    path('password/reset/', UserPasswordResetView.as_view(), name='password-reset'),
    path('password/reset/done/', UserPasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password/reset/confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),
    path('password_reset/complete/', UserPasswordResetCompleteView.as_view(), name='password-reset-complete'),
]
