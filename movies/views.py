from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import MovieCreationForm, ProgramCreationForm
from .models import ProgramModel

from datetime import datetime, timedelta


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
    context = {}

    if request.method == "GET":
        # Todays date
        today = (datetime.now().strftime(r'%m-%d'), datetime.now().strftime(r'%A'))
        days = []
        # Dates for next 14 days
        for x in range(1,14):
            next = datetime.now() + timedelta(days=x)
            days.append((next.strftime(r'%m-%d'), next.strftime(r'%A')))
        # Get the movies from today session
        program = ProgramModel.objects.filter(date__date=datetime.now().strftime(r'%Y-%m-%d'))
        context['program'] = program
        context['today'] = today
        context['days'] = days
    else:
        pass
    return render(request, 'movies/home_page_beta.html', context)