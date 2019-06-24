from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTestCase(TestCase):

    def test_create_user_with_email_successful(self):
        """Create a new user with an email is successful"""
        email = 'admin@example.com'
        password = 'password'
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))
