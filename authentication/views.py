from django.shortcuts import render, redirect
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from helpers.decorators import auth_user_should_not_access

# The auth_user_should_not_access decorator is used to prevent authenticated users from accessing this page
@auth_user_should_not_access
def register(request):
    if request.method == "POST":
        # Initialize context dictionary to store any errors and the user input data
        context = {'has_error': False, 'data': request.POST}
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Validate the password length
        if len(password) < 6 :
            messages.add_message(request, messages.ERROR, 'Your password should have at least 6 characters')
            context['has_error'] = True

        # Validate that the passwords match
        if password != password2 :
            messages.add_message(request, messages.ERROR, 'Passwords do not match')
            context['has_error'] = True

        # Validate the email format
        if not validate_email(email) :
            messages.add_message(request, messages.ERROR, 'Enter a valid email address')
            context['has_error'] = True

        # Validate that a username was provided
        if not username :
            messages.add_message(request, messages.ERROR, 'Username is required')
            context['has_error'] = True

        # Validate that the username is not already taken
        if User.objects.filter(username = username).exists() :
            messages.add_message(request, messages.ERROR, 'Username is already taken')
            context['has_error'] = True

            return render(request, 'authentication/register.html', context, status=409)

        # Validate that the email is not already in use
        if User.objects.filter(email = email).exists() :
            messages.add_message(request, messages.ERROR, 'E-mail is already taken')
            context['has_error'] = True

            return render(request, 'authentication/register.html', context, status=409)

        # If there are any errors, re-render the form with error messages
        if context['has_error'] :
            return render(request, 'authentication/register.html', context)
        
        # Create a new user object and save it to the database
        user = User.objects.create_user(username = username, email = email)
        user.set_password(password)
        user.save()

        # Display a success message and redirect to the login page
        messages.add_message(request, messages.SUCCESS, 'Account created successfully')

        return redirect('login')

    # If the request method is not POST, render the registration form
    return render(request, 'authentication/register.html')

@auth_user_should_not_access
def login_user(request):

    if request.method == "POST":
        context = {'data' : request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username = username, password = password)

        # If authentication fails, display an error message
        if not user :
            messages.add_message(request, messages.ERROR, 'Invalid crdentials')

            return render(request, 'authentication/login.html', context)
        
        # If authentication is successful, log the user in and redirect to the home page
        login(request, user)

        messages.add_message(request, messages.SUCCESS, f'Welcome {user.username}')

        return redirect(reverse('home'))
    
    # If the request method is GET, render the login page.
    return render(request, 'authentication/login.html')

# This function logs the user out and redirects to the login page.
def logout_user(request):
    logout(request)

    messages.add_message(request, messages.SUCCESS, 'Successfully logged out')

    return redirect(reverse('login'))