from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from .serializers import ContactSerializer
from contacts.models import Contact
from users.models import CustomUser


# Create your views here.
class ContactViewset(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


"""
# Create your views here.
class CustomUserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ContactSerializer
"""


class ContactListAPIView(ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
