from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import MovieCreationForm, ProgramCreationForm


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
        form = MovieCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movies:create_movie')
        else:
            context['form'] = form
    else:
        form = MovieCreationForm()
        context['form'] = form
    
    return render(request, 'movies/create_movie.html', context)

def create_program_view(request):
    """
    Create new movie session
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
        form = ProgramCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies:create_program')
        else:
            context['form'] = form
    else:
        form = ProgramCreationForm()
        context['form'] = form
    
    return render(request, 'movies/create_program.html', context)

def homepage_view(request):
    return render(request, 'movies/home_page.html')