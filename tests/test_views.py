from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser
from contacts.models import Contact
import json


class TestViews(TestCase):
    def test_view(self):
        client = Client()