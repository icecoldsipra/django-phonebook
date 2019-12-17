from contacts.models import Contact
from users.models import CustomUser
from rest_framework.serializers import (
    ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
)


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('pk', 'email', 'first_name', 'last_name', 'mobile', 'city', 'image', 'date_joined', 'last_login',
                  'is_active', 'is_staff', 'is_admin')


contact_url = HyperlinkedIdentityField(
    view_name='contacts-view-api',
    lookup_field='pk'
)


class ContactSerializer(ModelSerializer):
    contact_url = contact_url
    """
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
        fields = ('contact_url', 'pk', 'first_name', 'last_name', 'email', 'mobile', 'city', 'image', 'date_added',
                  'date_updated')
