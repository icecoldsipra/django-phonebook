from django.contrib.auth import user_logged_in, user_logged_out
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import CustomUser, LoggedInUser
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from users.views import get_user_location


@receiver(pre_delete, sender=CustomUser)
def save_superuser(sender, instance, **kwargs):
    """
    Prevent admin members from deleting superuser account
    """
    if instance.is_admin:
        raise PermissionDenied


@receiver(user_logged_in)
def login_ip(sender, user, request, **kwargs):
    if user.is_authenticated:
        user.ip_address = get_user_location(request)['ip']
        user.user_agent = get_user_location(request)['user_agent']
        user.region = get_user_location(request)['region']

        if user.activation_date is None or user.activation_date == '':
            user.activation_date = timezone.now()

    user.save()


@receiver(user_logged_in)
def on_user_logged_in(sender, user, **kwargs):
    LoggedInUser.objects.get_or_create(user=user)
    #user.slug = CustomUser.slug
    #print((slug)


@receiver(user_logged_out)
def on_user_logged_out(sender, user, **kwargs):
    LoggedInUser.objects.filter(user=user).delete()
