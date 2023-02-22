from django.urls import path
from . import views

# Define URL patterns for the anime app
urlpatterns = [
    # Home page URL
    path('', views.index, name='home'),
    # URL for creating an anime review
    path('create/', views.create_anime_review, name='create-anime-review'),
    # URL for viewing anime details
    path('anime/<id>/', views.anime_detail, name='anime'),
    # URL for deleting an anime review
    path('anime-delete/<id>/', views.anime_delete, name='anime-delete'),
    # URL for editing an anime review
    path('anime-edit/<id>/', views.anime_edit, name='anime-edit'),
]
