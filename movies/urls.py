from django.urls import path
from .views import create_movie_view, create_program_view, homepage_view

app_name = 'movies'

urlpatterns = [
    path('add_movie/', create_movie_view, name='create_movie'),
    path('add_program/', create_program_view, name='create_program'),
]