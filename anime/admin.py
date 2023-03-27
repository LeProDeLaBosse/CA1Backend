from django.contrib import admin
from .models import Anime

class AnimeAdmin(admin.ModelAdmin):

    # define the fields to be displayed in the admin list view
    list_display=('title','description','is_completed')
    # define the fields to be searched in the admin search bar
    search_fields =('title','description','is_completed')
    # define the number of items to be displayed per page in the admin list view
    list_per_page=25
    
# register the Anime model with the AnimeAdmin customizations
admin.site.register(Anime,AnimeAdmin)