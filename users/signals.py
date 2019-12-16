from django.contrib.auth import user_logged_in, user_logged_out
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import CustomUser, LoggedInUser
from django.utils import timezone
from django.core.exceptions import PermissionDenied


#@receiver(pre_save, sender=CustomUser)
#def save_superuser(sender, instance, **kwargs):
#    """
#    Prevent staff members from updating/changing superuser access
#    """
#    if instance.is_admin:
#        raise PermissionDenied

# @receiver(post_save, sender=CustomUser)
# def add_deadline(sender, instance, **kwargs):
#    """
#    If a new user is added from Admin panel, automatically set below attributes to None
#    """
#    if sender.is_admin or sender.is_staff:
#        instance.is_active = True
#        instance.activation_status = True
#        instance.activation_deadline = None
#        instance.activation_date = timezone.now()


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
