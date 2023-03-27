from django.shortcuts import render
from .forms import AnimeForm
from .models import Anime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection

# Define a helper function to filter Anime objects based on the 'filter' GET parameter of the request
def get_showing_animes(request, animes):

    # Check if a 'filter' GET parameter is present in the request
    if request.GET and request.GET.get('filter'):
        # Filter Anime objects based on the 'filter' parameter value
        if request.GET.get('filter') == 'complete':
            return animes.filter(is_completed = True)
        if request.GET.get('filter') == 'incomplete':
            return animes.filter(is_completed = False)
    # Return all Anime objects if no 'filter' parameter is present in the request
    return animes

# The login_required decorator is used to ensure that only authenticated users can access this view
@login_required
def index(request):
    # Retrieve all Anime objects from the database that belong to the current user
    animes=Anime.objects.filter(owner=request.user)

    # Count the number of completed and incompleted Anime objects
    completed_count = animes.filter(is_completed = True).count()
    incompleted_count = animes.filter(is_completed = False).count()
    all_count = animes.count()
    
    # Define the context dictionary with the Anime objects and the count of completed and incompleted Anime objects
    context = {'animes': get_showing_animes(request, animes), 'all_count': all_count, 'completed_count': completed_count, 
               'incompleted_count': incompleted_count}
    # Render the index.html template with the retrieved Anime objects   
    return render(request, 'anime/index.html', context)

@login_required
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

        # Update the properties of the retrieved Anime object with the new values
        anime.title = title
        anime.description = description
        anime.is_completed = True if is_completed== "on" else False
        anime.owner = request.user
        # Save the new Anime instance to the database
        anime.save()

        # Add a success message to the messages framework to be displayed on the next page
        messages.add_message(request, messages.SUCCESS, "Anime created successfully")

        # Redirect to the detail view for the newly created Anime instance
        return HttpResponseRedirect(reverse("anime", kwargs={'id': anime.pk}))

    # Render the create-anime-review.html template with the AnimeForm instance
    return render(request, 'anime/create-anime-review.html', context)

@login_required
def anime_detail(request, id):
    # Retrieve the Anime object with the given id, or display a 404 error if it doesn't exist
    anime = get_object_or_404(Anime, pk=id)
    context = {'anime': anime}
    # Render the anime-detail.html template with the retrieved Anime object
    return render(request, 'anime/anime-detail.html', context)

@login_required
def anime_delete(request, id):
    # Retrieve the Anime object with the given id, or display a 404 error if it doesn't exist
    anime = get_object_or_404(Anime, pk=id)
    context = {'anime': anime}

    if request.method == 'POST':
        # Check if the logged in user is the owner of the Anime object
        if anime.owner == request.user:

            # If the request method is POST, delete the Anime object and redirect to the home view
            anime.delete()

            # Add a success message to the messages framework to be displayed on the next page
            messages.add_message(request, messages.SUCCESS, "Anime deleted successfully")

            return HttpResponseRedirect(reverse('home'))
        
        # If the user is not the owner, display the anime-delete.html template with the retrieved Anime object
        return render(request, 'anime/anime-delete.html', context)
    
    # If the request method is not POST, render the anime-delete.html template with the retrieved Anime object
    return render(request, 'anime/anime-delete.html', context)

@login_required
def anime_edit(request, id):
    # Retrieve the Anime object with the given id from the database
    anime = get_object_or_404(Anime, pk=id)
    # Create a form instance with the retrieved Anime object
    form = AnimeForm(instance = anime)
    # Create a context dictionary containing the Anime object and the form instance
    context = {'anime': anime, 'form': form}

    if request.method == 'POST':
        # Get the form data from the request
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)

        # Update the properties of the retrieved Anime object with the new values
        anime.title = title
        anime.description = description
        anime.is_completed = True if is_completed== "on" else False

        if anime.owner == request.user:
            # Save the new Anime instance to the database
            anime.save()

        messages.add_message(request, messages.SUCCESS, "Anime update success")

        # Redirect to the detail view for the newly created Anime instance
        return HttpResponseRedirect(reverse("anime", kwargs={'id': anime.pk}))

    return render(request, 'anime/anime-edit.html', context)

def my_view(request):
    # Get the user ID from the request parameters
    user_id = request.GET.get('user_id')

    # Use a parameterized query to avoid SQL injection
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM myapp_user WHERE id = %s", [user_id])
        user = cursor.fetchone()

    return render(request, 'myapp/user_detail.html', {'user': user})

from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def my_view(request):
    # Get the redirect URL from the request parameters
    redirect_url = request.GET.get('redirect_url')

    # Check if the redirect URL is valid
    if 'http' in redirect_url:
        return HttpResponseRedirect('/invalid-redirect-url/')
    
    # Redirect to the internal URL
    return redirect(redirect_url)