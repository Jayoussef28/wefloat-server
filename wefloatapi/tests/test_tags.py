from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker
from wefloatapi.models import Tag
from .utils import create_data, refresh_data

class TestTags(APITestCase):
    faker = Faker()

    @classmethod
    def setUpTestData(cls):
        """Set up reusable test data."""
        create_data(cls)

    def setUp(self):
        """Refresh data before each test."""
        refresh_data(self)

    def test_create(self):
        """Test creating a new Tag object via API."""
        new_tag = {
            "name": self.faker.word(),  # Generate a random tag name
        }

        response = self.client.post("/tags", new_tag, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data
        self.assertTrue("id" in data)
        self.assertTrue("name" in data)

        db_tag = Tag.objects.get(pk=data["id"])
        self.assertEqual(db_tag.name, new_tag["name"])

    def test_delete(self):
        """Test deleting a Tag object."""
        tag_id = Tag.objects.all()[0].id
        response = self.client.delete(f"/tags/{tag_id}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        tags = Tag.objects.filter(id=tag_id)
        self.assertEqual(len(tags), 0)

    def test_update(self):
        """Test updating a Tag object."""
        tag_id = Tag.objects.all()[0].id
        updated_tag = {
            "name": self.faker.word(),  # Generate a fake updated tag name
        }

        response = self.client.put(f"/tags/{tag_id}", updated_tag, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertTrue("id" in data)
        self.assertTrue("name" in data)

        db_tag = Tag.objects.get(pk=tag_id)
        self.assertEqual(db_tag.name, updated_tag["name"])

    def test_list(self):
        """Test retrieving a list of Tag objects."""
        response = self.client.get("/tags")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data), len(self.tags))  # Compare length with created tags

        first_tag = data[0]
        self.assertTrue("id" in first_tag)
        self.assertTrue("name" in first_tag)

    def test_details(self):
        """Test retrieving a single Tag object."""
        tag_instance = Tag.objects.all()[0]
        response = self.client.get(f"/tags/{tag_instance.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["id"], tag_instance.id)
        self.assertEqual(data["name"], tag_instance.name)
