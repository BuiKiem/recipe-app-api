from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTestCase(TestCase):
    """Test the user API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Create user with valid payload is successful."""
        payload = {
            'email': 'user@example.com',
            'password': 'password',
            'name': 'name',
        }

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_create_with_used_email(self):
        """Create user with already used email is fail."""
        payload = {
            'email': 'user@example.com',
            'password': 'password',
        }
        create_user(**payload)

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_password_too_short(self):
        """Password must be more than 5 characters."""
        payload = {
            'email': 'user@example.com',
            'password': 'pw',
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        user_exists = get_user_model().objects.filter(email=payload['email']).exists()

        self.assertFalse(user_exists)
