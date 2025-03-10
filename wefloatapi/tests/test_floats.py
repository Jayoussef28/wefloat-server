from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker

from wefloatapi.models import Float, User, Difficulty, Rating
from .utils import create_data, refresh_data


class TestFloats(APITestCase):
    faker = Faker()

    @classmethod
    def setUpTestData(cls):
        """Set up reusable test data."""
        create_data(cls)

    def setUp(self):
        """Refresh data before each test."""
        refresh_data(self)

    def test_create(self):
        """Test creating a new Float object via API."""
        new_float = {
            "name": self.faker.word(),
            "location": self.faker.city(),
            "author": self.users[0].id, 
            "description": self.faker.sentence(nb_words=10),
            "distance": f"{self.faker.random_int(min=1, max=100)} miles",
            "difficulty": self.difficulty.id,
            "image": self.faker.image_url(),
            "rating": self.rating.id,
        }

        response = self.client.post("/floats", new_float, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data
        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertTrue("location" in data)
        self.assertTrue("description" in data)
        self.assertTrue("distance" in data)

        db_float = Float.objects.get(pk=data["id"])
        self.assertEqual(db_float.name, new_float["name"])
        self.assertEqual(db_float.location, new_float["location"])
        self.assertEqual(db_float.description, new_float["description"])
        self.assertEqual(db_float.distance, new_float["distance"])

    def test_delete(self):
        """Test deleting a Float object."""
        float_id = Float.objects.all()[0].id
        response = self.client.delete(f"/floats/{float_id}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        floats = Float.objects.filter(id=float_id)
        self.assertEqual(len(floats), 0)

    def test_update(self):
        """Test updating a Float object."""
        float_id = Float.objects.all()[0].id
        updated_float = {
            "name": self.faker.word(),
            "location": self.faker.city(),
            "author": self.users[0].id, 
            "description": self.faker.sentence(nb_words=15),
            "distance": f"{self.faker.random_int(min=1, max=100)} miles",
            "difficulty": self.difficulty.id,
            "image": self.faker.image_url(),
            "rating": self.rating.id,
        }

        response = self.client.put(f"/floats/{float_id}", updated_float, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertTrue("location" in data)
        self.assertTrue("description" in data)

        db_float = Float.objects.get(pk=float_id)
        self.assertEqual(db_float.name, updated_float["name"])
        self.assertEqual(db_float.location, updated_float["location"])
        self.assertEqual(db_float.description, updated_float["description"])

    def test_list(self):
        """Test retrieving a list of Float objects."""
        response = self.client.get("/floats")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data), len(self.floats))

        first_float = data[0]
        self.assertTrue("id" in first_float)
        self.assertTrue("name" in first_float)
        self.assertTrue("location" in first_float)
        self.assertTrue("description" in first_float)

    def test_details(self):
        """Test retrieving a single Float object."""
        float_instance = Float.objects.all()[0]
        response = self.client.get(f"/floats/{float_instance.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["id"], float_instance.id)
        self.assertEqual(data["name"], float_instance.name)
        self.assertEqual(data["location"], float_instance.location)
        self.assertEqual(data["description"], float_instance.description)
