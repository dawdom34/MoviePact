from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from .forms import AccountAuthenticationForm, AccountRegisterForm

# Create your views here.
def login_view(request):
    """
    Login user
    """
    context = {}
    user = request.user
    # Check if user is already authenticated
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        # Define form
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            # Get email and password from form
            email = request.POST['email']
            password = request.POST['password']
            # Authentoicate and login user
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')
        else:
            context['form'] = form
            return render(request, 'users/login.html', context)
    else:
        form = AccountAuthenticationForm()
        context['form'] = form
        return render(request, 'users/login.html', context)

def register_view(request):
    """
    Register user
    """
    context = {}
    user = request.user
    # Check if user is already authenticated
    if user.is_authenticated:
        return HttpResponse(f'You are already authenticated as {user.email}.')
    if request.POST:
        # Define form
        form  = AccountRegisterForm(request.POST)
        if form.is_valid():
            # Save the form
            form.save()
            # Get email and raw password from the form
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password1']
            # Authenticate user and login
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            context['form'] = form
    else:
        form = AccountRegisterForm()
        context['form'] = form

    return render(request, 'users/register.html', context)

    return render(request, 'users/register.html')

def logout_view(request):
    """
    Logout user
    """
    logout(request)
    return redirect('login')