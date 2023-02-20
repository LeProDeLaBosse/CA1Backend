from django import forms
from .models import Anime

class AnimeForm(forms.ModelForm):

    # this form is built on the Anime model
    class Meta:
        model = Anime
        # include all fields from the Anime model
        fields= "__all__"