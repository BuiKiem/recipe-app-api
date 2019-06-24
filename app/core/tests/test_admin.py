from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(email='admin@example.com', password='password')
        self.user = get_user_model().objects.create_user(email='user1@example.com', password='password', name='User 1')
        self.client.force_login(self.admin_user)

    def test_user_list_page(self):
        """Users are listed on user page."""
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_edit_page(self):
        """User edit page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])  # example: /admin/core/user/1
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

    def test_user_create_page(self):
        """User create page works."""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
