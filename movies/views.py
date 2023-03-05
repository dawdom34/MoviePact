from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import MovieCreationForm


def create_movie_view(request):
    """
    Add new movie to database
    """
    context = {}
    user = request.user

    # Check if user is authenticated
    if not user.is_authenticated:
        return redirect('login')
    
    # Check if user has staff privileges
    if not user.is_staff:
        return HttpResponse('Acces denied!')
    
    if request.POST:
        form = MovieCreationForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('movies:create_movie')
        else:
            context['form'] = form
    else:
        form = MovieCreationForm()
        context['form'] = form
    
    return render(request, 'movies/create_movie.html', context)