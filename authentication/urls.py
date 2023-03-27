from django.urls import path
from . import views

# Define the URL patterns for the accounts app
urlpatterns = [
    # URL for log in
    path('login', views.login_user, name='login'),
    # URL for register
    path('register', views.register, name='register'),
    # URL for log out
    path('logout_user', views.logout_user, name='logout_user'),
    # URL for activate account
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
]