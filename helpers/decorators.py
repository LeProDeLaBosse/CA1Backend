from django.contrib.auth.decorators import user_passes_test

# Define a function to check if a user is logged out
def check_user(user):
    return not user.is_authenticated

# Decorator that checks if the user is logged out, redirecting to '/' if logged in
user_logout_required = user_passes_test(check_user, '/', None)

# Decorator that uses the 'user_logout_required' decorator to ensure that the user is logged out
def auth_user_should_not_access(viewfunc):
    return user_logout_required(viewfunc)