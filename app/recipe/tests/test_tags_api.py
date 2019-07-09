from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Recipe
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTestCase(TestCase):
    """Test the publicly of tags API."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test that log in is required for retrieving tags."""
        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTestCase(TestCase):
    """Test the authorized user tags API."""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(email='user@example.com', password='password')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags is successful."""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_owner(self):
        """Test that tags returned are only belong to the authenticated user."""
        other_user = get_user_model().objects.create_user(email='other@example.com', password='password')
        tag = Tag.objects.create(user=self.user, name='Fruity')
        Tag.objects.create(user=other_user, name='Comfort Food')

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag."""
        payload = {'name': 'Test tag'}

        response = self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(user=self.user, name=payload['name']).exists()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload."""
        payload = {'name': ''}

        response = self.client.post(TAGS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tags_belongs_to_recipe(self):
        """Filtering tags that are belong to recipe."""
        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Lunch')
        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)
        recipe = Recipe.objects.create(title='Coriander eggs on toast', time_minutes=10, price=5.00, user=self.user)
        recipe.tags.add(tag1)

        response = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_retrive_unique_tags(self):
        """Filtering tags by assigned returns unique item."""
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        Tag.objects.create(user=self.user, name='Lunch')
        recipe1 = Recipe.objects.create(title='Pancake', time_minutes=5, price=3.00, user=self.user)
        recipe1.tags.add(tag)
        recipe2 = Recipe.objects.create(title='Porridge', time_minutes=3, price=2.00, user=self.user)
        recipe2.tags.add(tag)

        response = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(response.data), 1)

