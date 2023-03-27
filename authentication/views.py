from django.shortcuts import render, redirect
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from helpers.decorators import auth_user_should_not_access
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading

class EmailThread(threading.Thread):

    # A thread to send emails in the background
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    # Send email to activate user's account
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('authentication/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )
    
    # Start a new thread to send the email in the background
    if not settings.TESTING:
        EmailThread(email).start() 

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

        send_activation_email(user, request)

        # Display a success message and redirect to the login page
        messages.add_message(request, messages.SUCCESS, 'We sent you an email to verify your account')

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

        """if not user.is_email_verified:
            messages.add_message(request, messages.ERROR, 'Email is not verified, please check your email inbox')
            return render(request, 'authentication/login.html', context, status=401)"""

        # If authentication fails, display an error message
        if not user :
            messages.add_message(request, messages.ERROR, 'Invalid credentials')

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

def activate_user(request, uidb64, token):

    # Activate the user's account based on uid and token
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS, 'Email verified, you can now login')
        return redirect(reverse('login'))

    return render(request, 'authentication/activate-failed.html', {"user": user})