from django.db import models

# Create a base class for tracking created and updated timestamps for models that inherit from it
class TrackingModel(models.Model):
    # Add a created_at field that is automatically set to the current date and time when a new object is created
    created_at = models.DateTimeField(auto_now_add=True)
    # Add an updated_at field that is automatically updated with the current date and time whenever the object is saved
    updated_at = models.DateTimeField(auto_now=True)

    # Set the class as abstract so it can't be instantiated directly
    class Meta:
        abstract = True
        # Set the default ordering to be by the created_at field, in descending order
        ordering = ('-created_at',)