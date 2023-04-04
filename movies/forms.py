from django import forms
from .models import MovieModel, ProgramModel


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
    poster = forms.ImageField(required=False, initial='default-movie-poster.jpg')
    
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
    

class ProgramCreationForm(forms.ModelForm):

    date = forms.DateTimeField(widget=forms.DateTimeInput(format=r'%Y-%m-%d %H:%M:%S'),input_formats=[r'%Y-%m-%d %H:%M:%S'], help_text='YYYY-MM-DD HH:MM:SS')

    class Meta:
        model = ProgramModel
        fields = ('movie', 'date', 'price')

    def clean(self):
        """
        Check if given movie session at this time already exist
        """
        movie = self.cleaned_data['movie']
        date = self.cleaned_data['date']
        try:
            program = ProgramModel.objects.get(movie=movie, date=date)
        except ProgramModel.DoesNotExist:
            return self.cleaned_data
        raise forms.ValidationError('Program for this movie at this time already exist!')
