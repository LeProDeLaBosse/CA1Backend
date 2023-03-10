# Import necessary modules
from django.db import models
from authentication.models import User
from django.utils import timezone

# Define the Anime model
class Anime(models.Model):
    # Define fields for the model

    # CharField to store title of the anime
    title = models.CharField(max_length=255)
    # TextField to store a long description of the anime
    description = models.TextField()
    # BooleanField to track whether the anime has been completed or not
    is_completed = models.BooleanField(default=False)
    # A timestamp indicating the date and time when the anime was created
    created_at = models.DateTimeField(default=timezone.now())
    # A timestamp indicating the date and time when the anime was last updated
    updated_at = models.DateTimeField(default=timezone.now())

    owner = models.ForeignKey(to=User, on_delete=models.CASCADE) # ForeignKey to User model

    # Define the string representation of the model
    def __str__(self):
        return self.title
