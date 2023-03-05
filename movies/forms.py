from django import forms
from .models import MovieModel


class MovieCreationForm(forms.ModelForm):
    title = forms.CharField(max_length=255)
    description = forms.Textarea()
    trailer_link = forms.CharField(max_length=255)
    category = forms.CharField(max_length=200)
    duration = forms.IntegerField()
    age_category = forms.IntegerField()
    cast = forms.Textarea()
    release_date = forms.DateField()
    direction = forms.CharField(max_length=200)
    script = forms.CharField(max_length=200)
    poster = forms.ImageField(required=False)

    class Meta:
        model = MovieModel
        fields = ('title', 'description', 'trailer_link', 'category', 'duration',
                  'age_category', 'cast', 'release_date', 'direction', 'script', 
                  'poster')
        
    def clean_title(self):
        """
        Check if movie with this title already exist
        """
        title = self.cleaned_data['title']
        try:
            movie = MovieModel.objects.get(title=title)
        except MovieModel.DoesNotExist:
            return title
        raise forms.ValidationError(f'Movie with title "{title}" already exist!')
