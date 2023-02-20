from django.shortcuts import render
from .forms import AnimeForm
from .models import Anime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404

def index(request):
    # Retrieve all Anime objects from the database
    animes=Anime.objects.all()
    context = {'animes': animes} 
    # Render the index.html template with the retrieved Anime objects   
    return render(request, 'anime/index.html', context)

def create_anime_review(request):
    # Create an empty AnimeForm instance
    form = AnimeForm()
    context = {'form': form}

    if request.method == 'POST':
        # Get the form data from the request
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)

        # Create a new Anime instance and populate it with the form data
        anime=Anime()

        anime.title = title
        anime.description = description
        anime.is_completed = True if is_completed== "on" else False

        # Save the new Anime instance to the database
        anime.save()

        # Redirect to the detail view for the newly created Anime instance
        return HttpResponseRedirect(reverse("anime", kwargs={'id': anime.pk}))

    # Render the create-anime-review.html template with the AnimeForm instance
    return render(request, 'anime/create-anime-review.html', context)


def anime_detail(request, id):
    # Retrieve the Anime object with the given id, or display a 404 error if it doesn't exist
    anime = get_object_or_404(Anime, pk=id)
    context = {'anime': anime}
    # Render the anime-detail.html template with the retrieved Anime object
    return render(request, 'anime/anime-detail.html', context)

def anime_delete(request, id):
    # Retrieve the Anime object with the given id, or display a 404 error if it doesn't exist
    anime = get_object_or_404(Anime, pk=id)
    context = {'anime': anime}

    if request.method == 'POST':
        # If the request method is POST, delete the Anime object and redirect to the home view
        anime.delete()
        return HttpResponseRedirect(reverse('home'))
    
    # Render the anime-delete.html template with the retrieved Anime object
    return render(request, 'anime/anime-delete.html', context)