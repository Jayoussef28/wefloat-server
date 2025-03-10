from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker

from wefloatapi.models import Comment, User, Float, Rating
from .utils import create_data, refresh_data

class TestComments(APITestCase):
    faker = Faker()

    @classmethod
    def setUpTestData(cls):
        """Set up reusable test data."""
        create_data(cls)

    def setUp(self):
        """Refresh data before each test."""
        refresh_data(self)

    def test_create(self):
        """Test creating a new Comment object via API."""
        new_comment = {
            "float": self.floats[0].id,  # Use a float from the test data
            "commenter": self.users[0].id,  # Use the created user
            "rating": self.rating.id,  # Use the created rating
            "body": self.faker.sentence(nb_words=10),  # Generate a fake comment body
        }

        response = self.client.post("/comments", new_comment, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data
        self.assertTrue("id" in data)
        self.assertTrue("float" in data)
        self.assertTrue("commenter" in data)
        self.assertTrue("body" in data)

        db_comment = Comment.objects.get(pk=data["id"])
        self.assertEqual(db_comment.body, new_comment["body"])
        self.assertEqual(db_comment.float.id, new_comment["float"])
        self.assertEqual(db_comment.commenter.id, new_comment["commenter"])

    def test_delete(self):
        """Test deleting a Comment object."""
        comment_id = Comment.objects.all()[0].id
        response = self.client.delete(f"/comments/{comment_id}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        comments = Comment.objects.filter(id=comment_id)
        self.assertEqual(len(comments), 0)

    def test_update(self):
        """Test updating a Comment object."""
        comment_id = Comment.objects.all()[0].id
        updated_comment = {
            "float": self.floats[0].id,  # Use a float from the test data
            "commenter": self.users[0].id,  # Use the created user
            "rating": self.rating.id,  # Use the created rating
            "body": self.faker.sentence(nb_words=15),  # Generate a fake updated comment body
        }

        response = self.client.put(f"/comments/{comment_id}", updated_comment, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertTrue("id" in data)
        self.assertTrue("body" in data)

        db_comment = Comment.objects.get(pk=comment_id)
        self.assertEqual(db_comment.body, updated_comment["body"])
        self.assertEqual(db_comment.float.id, updated_comment["float"])
        self.assertEqual(db_comment.commenter.id, updated_comment["commenter"])

    def test_list(self):
        """Test retrieving a list of Comment objects."""
        response = self.client.get("/comments")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data), len(self.comments))

        first_comment = data[0]
        self.assertTrue("id" in first_comment)
        self.assertTrue("float" in first_comment)
        self.assertTrue("commenter" in first_comment)
        self.assertTrue("body" in first_comment)

    def test_details(self):
        """Test retrieving a single Comment object."""
        comment_instance = Comment.objects.all()[0]
        response = self.client.get(f"/comments/{comment_instance.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["id"], comment_instance.id)
        self.assertEqual(data["float"], comment_instance.float.id)
        self.assertEqual(data["commenter"], comment_instance.commenter.id)
        self.assertEqual(data["body"], comment_instance.body)
