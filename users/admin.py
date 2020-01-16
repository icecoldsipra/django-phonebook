from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from.forms import CustomUserCreationForm, CustomUserChangeForm


class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm  # To update view
    add_form = CustomUserCreationForm  # To create view

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'pk', 'slug', 'first_name', 'last_name', 'mobile', 'city', 'region', 'birthday',
                    'date_joined', 'email_sent', 'activation_deadline', 'activation_date', 'ip_address', 'user_agent',
                    'last_login', 'is_active', 'is_staff', 'is_admin')
    list_filter = ('is_active', 'is_staff', 'is_admin')

    # Break down how various fields appear in the Admin panel
    fieldsets = (
        (None, {'fields': ('email', 'password', 'date_joined', 'last_login', 'slug', 'ip_address', 'user_agent')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'mobile', 'city', 'region', 'birthday')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )

    search_fields = ('email', 'first_name', 'last_name', 'city', 'region')  # Add search bar in Admin panel
    ordering = ['-date_joined']  # Sort in descending order
    filter_horizontal = ()


# Reference the CustomUser model as User
User = get_user_model()

# Register models
admin.site.register(User, UserAdmin)

# Remove groups from Admin interface
admin.site.unregister(Group)

admin.site.site_header = "Phonebook Manager"
admin.site.site_title = "Phonebook Manager Portal"
admin.site.index_title = "Welcome to Django Phonebook Manager Portal!"
