from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ['pk', 'first_name', 'last_name', 'slug', 'email', 'mobile', 'city', 'birthday', 'date_added',
                    'date_updated', 'image', 'added_by']
    fields = [('first_name', 'last_name'), ('email', 'mobile'), 'city', 'birthday', 'image']


# Register your models here.
admin.site.register(Contact, ContactAdmin)
