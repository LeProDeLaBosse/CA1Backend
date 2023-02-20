"""AppAnime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# import admin module and url-related modules
from django.contrib import admin
from django.urls import path, include

# URL patterns
urlpatterns = [
    # path for accessing the built-in admin site
    path('admin/', admin.site.urls),
    # path for including the anime app's URLs
    path('', include('anime.urls')),
    # path for including the authentication app's URLs
    path('auth', include('authentication.urls'))
]
