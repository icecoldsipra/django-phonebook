from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from django.utils import timezone
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView,
)


# Enabling login for user
class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/users_login.html'
    success_message = "Welcome! You were successfully logged in."


# Enabling logout for user
class UserLogoutView(LogoutView):
    template_name = 'users/users_logout.html'
    #next_page = reverse_lazy('users-login')


class UserRegisterView(SuccessMessageMixin, CreateView):
    model = CustomUser
    template_name = 'users/users_register.html'
    form_class = CustomUserCreationForm
    #success_message = "An email has been sent to your email ID for verification."
    success_message = "Please sign in to access your account."
    success_url = reverse_lazy('users-login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.activation_deadline = timezone.now() + timezone.timedelta(days=7)
        user.is_active = True
        user.save()

        body = render_to_string(
            'registration/account_activation_email.html',
            {
                'user': user,
                'domain': self.request.get_host,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
        )
        subject = "Activate Your Account"
        to = form.cleaned_data['email']  # Get the email ID mentioned in registration form
        from_email = settings.EMAIL_HOST_USER

        # Send email to registered user
        send_email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[to],
        )
        
        send_email.content_subtype = "html"
        # send_email.send(fail_silently=False)

        return super().form_valid(form)


def users_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        token = default_token_generator.make_token(user)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.activation_status = True
        user.activation_date = timezone.now()
        user.activation_deadline = None
        user.save()

        #login(request, user)

        messages.success(request, "Your email has been verified successfully!")
        return redirect('users-login')
    else:
        messages.error(request, "Your email could not be verified.")
        # return render(request, 'account_activation_invalid.html')
        return render(request, 'users/users_login.html')


class UserPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    model = CustomUser
    form_class = CustomUserChangeForm


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    template_name = 'users/users_profile.html'
    form_class = CustomUserChangeForm
    success_message = "Profile updated successfully."


class UserPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password-reset-done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password-reset-complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
