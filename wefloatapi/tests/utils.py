from faker import Faker
from wefloatapi.models import User, Rating, Difficulty, Float, Comment, Tag

faker = Faker()

def create_data(cls):
    """
    Creates test data for the Float model, related dependencies, and User model.
    This function is called once before all tests in the class.
    """
    cls.faker = faker

    # Create a test user with full details
    cls.users = [
        User.objects.create(
            username=faker.user_name(),  # Generate a random username
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            image=faker.image_url(),  # Random image URL
            bio=faker.sentence(nb_words=15),  # Random bio sentence
            uid=faker.uuid4(),  # Random UUID for unique identification
        )
        for _ in range(5)  # Creates 5 user objects
    ]


    # Create a test rating
    cls.rating = Rating.objects.create(
        value=faker.random_int(min=1, max=5)
    )

    # Create a test difficulty level
    cls.difficulty = Difficulty.objects.create(
        name=faker.word()
    )
    
    cls.tags = [
        Tag.objects.create(name=faker.word()) for _ in range(5)  # Creates 5 tags
    ]

    # Create a list of test floats
    cls.floats = [
        Float.objects.create(
            name=faker.word(),
            location=faker.city(),
            author=cls.users[0],
            description=faker.sentence(),
            distance=str(faker.random_int(min=1, max=100)) + " miles",
            difficulty=cls.difficulty,
            rating=cls.rating
        )
        for _ in range(5)  # Creates 5 float objects
    ]

    # Create comments associated with the floats, users, and ratings
    cls.comments = [
        Comment.objects.create(
            float=cls.floats[faker.random_int(min=0, max=4)],  # Randomly associate a float
            commenter=cls.users[0],  # Use the created user as commenter
            rating=cls.rating,  # Use the created rating for the comment
            body=faker.sentence(),  # Generate a fake sentence as comment body
        )
        for _ in range(5)  # Creates 5 comment objects
    ]

def refresh_data(self):
    """
    Refreshes data before each test by retrieving the latest database state.
    This prevents stale object references.
    """
    self.users= list(User.objects.all())
    self.tags = list(Tag.objects.all())
    self.rating.refresh_from_db()
    self.difficulty.refresh_from_db()
    self.floats = list(Float.objects.all())
    self.comments = list(Comment.objects.all())  # Refresh the list of comments
