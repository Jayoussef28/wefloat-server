from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker

from wefloatapi.models import User
from .utils import create_data, refresh_data

class TestUsers(APITestCase):
    faker = Faker()

    @classmethod
    def setUpTestData(cls):
        """Set up reusable test data."""
        create_data(cls)

    def setUp(self):
        """Refresh data before each test."""
        refresh_data(self)

    def test_create(self):
        """Test creating a new User object via API."""
        new_user = {
            "username": self.faker.user_name(),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "image": self.faker.image_url(),
            "bio": self.faker.sentence(nb_words=10),
            "uid": self.faker.uuid4(),
        }

        response = self.client.post("/users", new_user, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data
        self.assertTrue("id" in data)
        self.assertTrue("username" in data)
        self.assertTrue("first_name" in data)
        self.assertTrue("last_name" in data)
        self.assertTrue("bio" in data)
        self.assertTrue("uid" in data)

        db_user = User.objects.get(pk=data["id"])
        self.assertEqual(db_user.username, new_user["username"])
        self.assertEqual(db_user.first_name, new_user["first_name"])
        self.assertEqual(db_user.last_name, new_user["last_name"])
        self.assertEqual(db_user.bio, new_user["bio"])
        self.assertEqual(db_user.uid, new_user["uid"])

    def test_delete(self):
        """Test deleting a User object."""
        user_id = User.objects.all()[0].id
        response = self.client.delete(f"/users/{user_id}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        users = User.objects.filter(id=user_id)
        self.assertEqual(len(users), 0)

    def test_update(self):
        """Test updating a User object."""
        user_id = User.objects.all()[0].id
        updated_user = {
            "username": self.faker.user_name(),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "image": self.faker.image_url(),
            "bio": self.faker.sentence(nb_words=15),
            "uid": self.faker.uuid4(),
        }

        response = self.client.put(f"/users/{user_id}", updated_user, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertTrue("id" in data)
        self.assertTrue("username" in data)
        self.assertTrue("first_name" in data)
        self.assertTrue("last_name" in data)
        self.assertTrue("bio" in data)
        self.assertTrue("uid" in data)

        db_user = User.objects.get(pk=user_id)
        self.assertEqual(db_user.username, updated_user["username"])
        self.assertEqual(db_user.first_name, updated_user["first_name"])
        self.assertEqual(db_user.last_name, updated_user["last_name"])
        self.assertEqual(db_user.bio, updated_user["bio"])
        self.assertEqual(db_user.uid, updated_user["uid"])

    def test_list(self):
        """Test retrieving a list of User objects."""
        response = self.client.get("/users")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data), len(self.users))  # Assuming you have a `users` list from test data

        first_user = data[0]
        self.assertTrue("id" in first_user)
        self.assertTrue("username" in first_user)
        self.assertTrue("first_name" in first_user)
        self.assertTrue("last_name" in first_user)
        self.assertTrue("bio" in first_user)

    def test_details(self):
        """Test retrieving a single User object."""
        user_instance = User.objects.all()[0]
        response = self.client.get(f"/users/{user_instance.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["id"], user_instance.id)
        self.assertEqual(data["username"], user_instance.username)
        self.assertEqual(data["first_name"], user_instance.first_name)
        self.assertEqual(data["last_name"], user_instance.last_name)
        self.assertEqual(data["bio"], user_instance.bio)
        self.assertEqual(data["uid"], user_instance.uid)
