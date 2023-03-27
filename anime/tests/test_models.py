from utils.setup_test import TestSetup
from authentication.models import User
from anime.models import Anime

# Create a test class that inherits from TestSetup
class TestModel(TestSetup):

    # Test to create a user
    def test_should_create_user(self):
        # Create a test user
        user = self.create_test_user()
        # Create an anime object with the created user as the owner
        anime = Anime(owner=user, title="One Piece", description='shonen')
        anime.save()
        # Assert that the anime object's string representation is "One Piece"
        self.assertEqual(str(anime), 'One Piece')