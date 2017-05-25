from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from gw2_app import *

class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'user007',
            'password': 'xbond'}
        User.objects.create_user(**self.credentials)
    def test_login(self):
        response = self.client.post('/accounts/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)