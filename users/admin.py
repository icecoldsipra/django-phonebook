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
    list_display = ('email', 'username', 'first_name', 'last_name', 'mobile', 'city', 'date_joined',
                    'activation_status', 'activation_deadline', 'activation_date', 'last_login', 'is_active',
                    'is_staff', 'is_admin')
    list_filter = ('is_active', 'is_staff', 'is_admin')

    # Break down how various fields appear in the Admin panel
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'date_joined', 'last_login')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'mobile', 'city')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )

    search_fields = ('email', 'username', 'first_name', 'last_name', 'city')  # Add search bar in Admin panel
    ordering = ['-date_joined']  # Sort in descending order
    filter_horizontal = ()


User = get_user_model()  # Reference the CustomUser model as User

admin.site.register(User, UserAdmin)
