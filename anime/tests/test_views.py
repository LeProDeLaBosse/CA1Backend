from utils.setup_test import TestSetup
from authentication.models import User
from anime.models import Anime
from django.urls import reverse

# Define a TestModel class that inherits from TestSetup
class TestModel(TestSetup):

    # Define a test method that creates an anime
    def test_should_create_an_anime(self):

        # Create a test user
        user = self.create_test_user()
        # Log the user in by posting to the login endpoint
        self.client.post(reverse("login"), {
            'username': user.username,
            'password': 'password12!'
        })

        # Assert that there are no animes in the database yet
        animes = Anime.objects.all()

        self.assertEqual(animes.count(), 0)

        # Create an anime review by posting to the create-anime-review endpoint
        response = self.client.post(reverse('create-anime-review'), {
            'owner': user,
            'title': "MHA",
            'description': "Hero"
        })

        # Assert that the anime was successfully created
        updated_animes = Anime.objects.all()

        self.assertEqual(updated_animes.count(), 1)

        # Assert that the response status code is 302
        self.assertEqual(response.status_code, 302)