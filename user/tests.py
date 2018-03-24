from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from language.models import Language


class TestUser(TestCase):
    def setUp(self):
        self.client = Client()
        Language.objects.create(name="SPA")

    def test_signup(self):
        users = User.objects.all().exists()
        self.assertFalse(users)

        self.client.post(
            '/signup/',
            {'description': 'Hi, I am student',
             'place': 'Lima',
             'language': '1',
             'proficiency': 'novice',
             'username': 'periquita',
             'first_name': 'Periquita',
             'last_name': 'DosPalotes',
             'email': 'periquitax100pre@gmail.com',
             'password1': 'thisIsMyPass1!',
             'password2': 'thisIsMyPass1!',
             },
        )
        users = User.objects.all().exists()
        self.assertEqual(True, users)

        user = User.objects.all()[0]
        self.assertEqual(False, user.is_active)

    def test_signup__active_true(self):
        users = User.objects.all().exists()
        self.assertFalse(users)

        self.client.post(
            '/signup/',
            {'description': 'Hi, I am student',
             'place': 'Lima',
             'language': '1',
             'proficiency': 'novice',
             'username': 'periquita',
             'first_name': 'Periquita',
             'last_name': 'DosPalotes',
             'email': 'periquitax100pre@gmail.com',
             'password1': 'thisIsMyPass1!',
             'password2': 'thisIsMyPass1!',
             'user.is_active': True,
             },
        )
        users = User.objects.all().exists()
        self.assertTrue(users)

        user = User.objects.all()[0]
        self.assertFalse(user.is_active)
