# Import necessary modules
from django.db import models
from authentication.models import User

# Define the Anime model
class Anime(models.Model):
     # Define fields for the model
    title = models.CharField(max_length=255) # CharField to store title of the anime
    description = models.TextField() # TextField to store a long description of the anime
    is_completed = models.BooleanField(default=False) # BooleanField to track whether the anime has been completed or not
    # owner = models.ForeignKey(to=User, on_delete=models.CASCADE) # ForeignKey to User model

    # Define the string representation of the model
    def __str__(self):
        return self.title
