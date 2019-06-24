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

    def test_new_user_email_normalized(self):
        """Email for new user is normalized."""
        email = 'admin@EXAMPLE.COM'
        password = 'password'
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(email.lower(), user.email)

    def test_new_user_with_invalid_email(self):
        """Create user with invalid email raises error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password='password')

    def test_create_new_super_user(self):
        """Create a new super user is successful."""
        user = get_user_model().objects.create_superuser(email='super@example.com', password='password')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
