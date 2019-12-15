from rest_framework import serializers
from contacts.models import Contact
from users.models import CustomUser


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('pk', 'first_name', 'last_name', 'email', 'mobile', 'city', 'image', 'url')


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ('pk', 'first_name', 'last_name', 'email', 'mobile', 'city', 'image', 'url')
