from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # Add any required additional fields required for signup.
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    password = None  # Required to exclude the password field in form

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'mobile', 'city', 'birthday', 'image')
