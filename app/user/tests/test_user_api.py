from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_USER = reverse('user:token')


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

    def test_create_token_for_user(self):
        """A token is created for user."""
        payload = {
            'email': 'user@example.com',
            'password': 'password',
        }
        create_user(**payload)

        response = self.client.post(TOKEN_USER, payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn('token', response.data)

    def test_create_token_invalid_credentials(self):
        """A token is NOT created if invalid credentials are given."""
        create_user(email='user@example.com', password='password')
        payload = {
            'email': 'user@example.com',
            'password': 'wrong',
        }

        response = self.client.post(TOKEN_USER, payload)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertNotIn('token', response.data)

    def test_create_token_no_user(self):
        """A token is NOT created if user doesn't exist."""
        payload = {
            'email': 'user@example.com',
            'password': 'password',
        }

        response = self.client.post(TOKEN_USER, payload)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertNotIn('token', response.data)

    def test_create_token_missing_field(self):
        """Both email and password are required to create token."""
        payload = {
            'email': 'user@example.com',
        }

        response = self.client.post(TOKEN_USER, payload)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertNotIn('token', response.data)
