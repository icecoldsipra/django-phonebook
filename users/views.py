from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserPasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import CustomUser
from django.utils import timezone
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)


# Enabling login for user
class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/users_login.html'
    success_message = "Welcome! You were successfully logged in."


# Enabling logout for user
class UserLogoutView(LogoutView):
    template_name = 'users/users_logout.html'


class UserRegisterView(SuccessMessageMixin, CreateView):
    model = CustomUser
    template_name = 'users/users_register.html'
    form_class = CustomUserCreationForm
    success_message = "An email has been sent to your email ID '%(email)s' for verification."
    success_url = reverse_lazy('users-login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.activation_deadline = timezone.now() + timezone.timedelta(days=7)
        user.email_sent = True
        user.is_active = False
        user.save()

        subject = f"DjangoPhonebook | Activate Your Account | {form.cleaned_data['email']}"
        to = form.cleaned_data['email']
        from_email = settings.EMAIL_HOST_USER
        body = render_to_string(
            'registration/account_activation_email.html', {
                'user': user,
                'domain': self.request.get_host,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
        )

        # Send email to registered user
        send_email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[to],
        )
        
        send_email.content_subtype = "html"
        send_email.send(fail_silently=False)

        return super().form_valid(form)


def users_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        token = default_token_generator.make_token(user)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.validation_token = f"{uidb64} : {token}"
        user.is_active = True
        user.activation_date = timezone.now()
        user.save()

        messages.success(request, "Your email has been verified successfully! Please login to access the website.")
        return redirect('users-login')
    else:
        messages.error(request, "Your email could not be verified. Please contact the site Admin.")
        return render(request, 'users/users_login.html')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    template_name = 'users/users_profile.html'
    form_class = CustomUserChangeForm
    success_message = "Profile updated successfully."

    # To ensure that only the logged in user has access to his content
    def test_func(self):
        obj = self.get_object()
        if self.request.user.email == obj.email:
            return True
        return False


class UserPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    model = CustomUser
    form_class = UserPasswordChangeForm
    template_name = 'registration/password_change_form.html'


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
