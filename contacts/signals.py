from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Contact


@receiver(post_save, sender=Contact)
def add_contact_details(sender, instance, created, **kwargs):
    """
    If a new contact is added, automatically update the added_by field
    """

    if created:
        if instance.added_by is None:
            instance.added_by = kwargs.get('user')
