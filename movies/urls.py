from django.urls import path
from .views import create_movie_view

app_name = 'movies'

urlpatterns = [
    path('add_movie/', create_movie_view, name='create_movie'),
]