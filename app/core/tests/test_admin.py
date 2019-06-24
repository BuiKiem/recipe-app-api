from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(email='admin@example.com', password='password')
        self.user = get_user_model().objects.create_user(email='user1@example.com', password='password', name='User 1')
        self.client.force_login(self.admin_user)

    def test_user_list(self):
        """Users are listed on user page."""
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)
