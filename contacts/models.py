from django.db import models
from django.utils import timezone
from django.conf import settings
from django.shortcuts import reverse
from django.utils.text import slugify


# Create your models here.
class Contact(models.Model):
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField("First Name", max_length=255, help_text="Enter First Name")
    last_name = models.CharField("Last Name", max_length=255, blank=True, default='', help_text="Enter Last Name")
    slug = models.SlugField("Slug", unique=True, max_length=255, default='')
    email = models.EmailField("Email", max_length=100, blank=True, default='', help_text="Enter Valid Email ID")
    mobile = models.CharField("Mobile", max_length=11, blank=True, default='', help_text="Enter Mobile Number")
    city = models.CharField("City", max_length=100, blank=True, default='', help_text="Enter City")
    birthday = models.DateField("Birthday", blank=True, null=True, help_text="Enter Birthday in YYYY-MM-DD Format")
    image = models.ImageField("Image", upload_to='contacts', default='default.png', blank=True,
                              help_text="Upload Profile Pic")
    date_added = models.DateTimeField("Date Added", default=timezone.now)
    date_updated = models.DateTimeField("Date Updated", default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        else:
            return self.first_name

    def get_short_name(self):
        if self.first_name:
            return self.first_name

    def get_absolute_url(self):
        return reverse('users-profile', kwargs={'slug': self.slug})

    def _get_unique_slug(self):
        slug = slugify(self.get_full_name())
        unique_slug = slug
        num = 1
        while Contact.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)