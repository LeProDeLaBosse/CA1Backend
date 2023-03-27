from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register the User model with the UserAdmin model in the Django admin site
admin.site.register(User, UserAdmin)