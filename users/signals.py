from django.contrib.auth import user_logged_in, user_logged_out
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import CustomUser, LoggedInUser
from django.utils import timezone
from django.core.exceptions import PermissionDenied


@receiver(pre_delete, sender=CustomUser)
def save_superuser(sender, instance, **kwargs):
    """
    Prevent admin members from deleting superuser account
    """
    if instance.is_admin:
        raise PermissionDenied


@receiver(post_save, sender=CustomUser)
def update_user(sender, instance, created, **kwargs):
    """
    If a new user is created, automatically update below attributes
    """
    if created and not instance.email_sent:
        instance.is_active = True
        instance.activation_date = timezone.now()


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
