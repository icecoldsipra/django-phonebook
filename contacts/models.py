from django.db import models
from django.utils import timezone
from django.conf import settings
from django.shortcuts import reverse
from django.utils.text import slugify


# Create your models here.
class Contact(models.Model):
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, default='')
    slug = models.SlugField(unique=True, max_length=100, default='')
    email = models.EmailField(max_length=100, blank=True, default='')
    mobile = models.CharField(max_length=11, default='', blank=True)
    city = models.CharField(max_length=25, default='', blank=True)
    birthday = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='contacts', default='default.png', blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)

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