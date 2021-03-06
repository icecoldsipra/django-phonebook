from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.utils.text import slugify


class CustomUserManager(BaseUserManager):
    # Specify all the required fields here
    def create_user(self, email, first_name, last_name, password, is_active=True, is_staff=False, is_admin=False,
                    **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        # Raise exception if user does not have an email
        if not email:
            raise ValueError("Users must provide an email address.")
        # Raise exception if user does not have a password
        if not password:
            raise ValueError("Users must enter a password.")
        # Raise exception if user does not enter a first name
        if not first_name:
            raise ValueError("Users must provide first name.")

        user = self.model(
            email=self.normalize_email(email),  # Converts all characters of email field to lower cases
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_staff=is_staff,
            is_admin=is_admin,
            **extra_fields

        )

        user.set_password(password)  # Change user password
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, password, **extra_fields):
        """
        Creates and saves a staff user with the given email and password.
        """

        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_active=True,
            is_staff=True,
            is_admin=False
        )
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """

        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_active=True,
            is_staff=True,
            is_admin=True
        )
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField("Email", unique=True, max_length=100, help_text="Enter Valid Email ID")
    first_name = models.CharField("First Name", max_length=255, help_text="Enter Your First Name")
    last_name = models.CharField("Last Name", max_length=255, blank=True, default='', help_text="Enter Your Last Name")
    slug = models.SlugField("Slug", unique=True, max_length=255, default='')
    mobile = models.CharField("Mobile", max_length=11, blank=True, default='', help_text="Enter Your Mobile Number")
    city = models.CharField("City", max_length=100, blank=True, default='', help_text="Enter Your City")
    region = models.CharField("Region", max_length=100, blank=True, default='')
    ip_address = models.CharField("IP Address", max_length=35, blank=True, default='')
    user_agent = models.CharField("User Agent", max_length=255, blank=True, default='')
    image = models.ImageField("Image", upload_to='users', default='default.png', blank=True,
                              help_text="Upload Your Profile Pic")
    birthday = models.DateField("Birthday", blank=True, null=True, help_text="Enter Your Birthday in YYYY-MM-DD Format")
    email_sent = models.BooleanField("Email Sent", blank=True, null=True, default=False)
    activation_deadline = models.DateTimeField("Activation Deadline", blank=True, null=True, default=None)
    activation_date = models.DateTimeField("Activation Date", blank=True, null=True, default=None)
    is_active = models.BooleanField("Is Active", default=True)  # Can login
    is_staff = models.BooleanField("Is Staff", default=False)  # staff but non-superuser
    is_admin = models.BooleanField("Is Admin", default=False)  # superuser
    date_joined = models.DateTimeField("Date Joined", default=timezone.now)  # Sets value to current date and time

    class Meta:
        verbose_name = 'Registered User'
        verbose_name_plural = 'Registered Users'

    # Username and password are required by default
    # set email as the default username for authentication
    USERNAME_FIELD = 'email'
    # Can add additional fields which will be asked during superuser creation
    # These fields should also be included in the create_user() function in CustomUserManager class
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    # def __str__(self):
    #    return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        else:
            return self.first_name

    def get_short_name(self):
        if self.first_name:
            return self.first_name

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        # Simplest possible answer: Yes, always
        return self.is_staff

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        # Simplest possible answer: Yes, always
        return self.is_staff

    def get_absolute_url(self):
        return reverse('users-profile', kwargs={'slug': self.slug})

    def _get_unique_slug(self):
        slug = slugify(self.get_full_name())
        unique_slug = slug
        num = 1
        while CustomUser.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


# Model to store the list of logged in users
class LoggedInUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='logged_in_user')
    # slug = models.SlugField("Slug", unique=True, max_length=255, default='')
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user

    """
    def get_absolute_url(self):
        return reverse('users-profile', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = CustomUser.slug
        super().save(*args, **kwargs)
    """
