from contacts.models import Contact
from users.models import CustomUser
from rest_framework.serializers import (
    ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
)


class CustomUserCreateSerializer(ModelSerializer):
    password1 = []

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True}
        }


class CustomUserProfileSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('pk', 'email', 'first_name', 'last_name', 'mobile', 'city', 'image', 'date_joined', 'last_login',
                  'is_active', 'is_staff', 'is_admin')


contact_url = HyperlinkedIdentityField(
    view_name='contacts-view-api',
    lookup_field='pk'
)


class ContactCreateSerializer(ModelSerializer):
    contact_url = contact_url

    class Meta:
        model = Contact
        fields = ('contact_url', 'first_name', 'last_name', 'email', 'mobile', 'city', 'image')

        extra_kwargs = {
            'first_name': {'required': True},
        }


class ContactSerializer(ModelSerializer):
    contact_url = contact_url
    """
    # Replaces numbers by actual values
    
    added_by = SerializerMethodField()
    image = SerializerMethodField()

    def get_added_by(self, obj):
        return str(obj.added_by)

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image
    """
    class Meta:
        model = Contact
        fields = ('contact_url', 'pk', 'slug', 'first_name', 'last_name', 'email', 'mobile', 'city', 'image',
                  'date_added', 'date_updated')
