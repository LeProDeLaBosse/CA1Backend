from django.shortcuts import render

# Handle HTTP 404 error
def handle_not_found(request, exception):
    return render(request, 'not-found.html')

# Handle HTTP 500 error
def handle_server_error(request):
    return render(request, 'server-error.html')