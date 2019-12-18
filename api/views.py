from contacts.models import Contact
from users.models import CustomUser
from django.utils import timezone
from .permissions import IsOwnerOrReadOnly
from .pagination import CustomLimitOffsetPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import (
    CustomUserProfileSerializer, CustomUserCreateSerializer, ContactSerializer, ContactCreateSerializer
)
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
)


# Endpoint to register new user
class CustomUserCreateAPIView(CreateAPIView):
    serializer_class = CustomUserCreateSerializer


# Endpoint with prefilled values to update one single contact of the logged in user
class CustomUserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = CustomUserProfileSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(email=self.request.user)


# Endpoint to create a new contact
class ContactCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ContactCreateSerializer

    def perform_create(self, serializer):
        serializer.save(
            added_by=self.request.user
        )


# Endpoint to list all contacts of the logged in user
class ContactListAPIView(ListAPIView):
    serializer_class = ContactSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'mobile', 'city']
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        return Contact.objects.filter(added_by=self.request.user).order_by('-date_added')


# Endpoint to list one single contact of the logged in user
class ContactRetrieveAPIView(RetrieveAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.filter(added_by=self.request.user)


# Endpoint with prefilled values to update one single contact of the logged in user
class ContactRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.filter(added_by=self.request.user).order_by('-date_added')

    def perform_update(self, serializer):
        serializer.save(
            date_updated=timezone.now()
        )


class ContactRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.filter(added_by=self.request.user).order_by('-date_added')
