from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

from .forms import MovieCreationForm, ProgramCreationForm
from .models import ProgramModel, SeatsModel, TicketsModel
from .utils import check_if_refundable

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
    """
    Get todays movie sessions
    """
    context = {}

    if request.method == "GET":
        # Todays date
        today = (datetime.now().strftime(r'%m-%d'), datetime.now().strftime(r'%A'), datetime.now().strftime(r'%Y-%m-%d'))
        days = []
        # Dates for next 14 days
        for x in range(1,14):
            next = datetime.now() + timedelta(days=x)
            days.append((next.strftime(r'%m-%d'), next.strftime(r'%A'), next.strftime(r'%Y-%m-%d')))
        # Get the movies from today session
        program = ProgramModel.objects.filter(date__date=datetime.now().strftime(r'%Y-%m-%d'))
        context['program'] = program
        context['today'] = today
        context['days'] = days
    else:
        pass
    return render(request, 'movies/home_page_beta.html', context)

def date_filter_view(request, *args, **kwargs):
    """
    Get movie sessions for selected day
    """
    context = {}

    if request.method == 'GET':
        # Todays date
        today = (datetime.now().strftime(r'%m-%d'), datetime.now().strftime(r'%A'), datetime.now().strftime(r'%Y-%m-%d'))
        days = []
        # Dates for next 14 days
        for x in range(1,14):
            next = datetime.now() + timedelta(days=x)
            days.append((next.strftime(r'%m-%d'), next.strftime(r'%A'), next.strftime(r'%Y-%m-%d')))
        # Get the movies from selected date
        date = kwargs.get('date')
        selected_date = datetime(year=int(date[0:4]), month=int(date[5:7]), day=int(date[8:]))
        program = ProgramModel.objects.filter(date__date=date)

        context['program'] = program
        context['today'] = today
        context['days'] = days
        context['selected_date'] = (selected_date.strftime(r'%m-%d'), selected_date.strftime(r'%A'))

    return render(request, 'movies/date_filter.html', context)

def movie_details_view(request, *args, **kwargs):
    """
    Get seance details
    """
    context = {}

    if request.method == 'GET':
        # Get seance id from url
        seance_id = kwargs.get('seance_id')
        # Get seance object with given id
        seance = ProgramModel.objects.get(id=seance_id)

        # check if the seance has vacancies
        # Get taken seats for given seance
        seats = SeatsModel.objects.filter(program=seance)
        taken_seats = ''
        # Append all seats numbers to the string
        for x in seats:
            taken_seats += x.seats_numbers + ','
        # Convert string to array
        taken_seats_arr = taken_seats.split(',')
        # Delete last argument from array, it's empty string
        taken_seats_arr.pop(-1)
        # Check if the length of array is equal 48 (the cinema hall has 48 seats available)
        if len(taken_seats_arr) == 48:
            tickets_sold_out = True
        else:
            tickets_sold_out = False

        context['seance'] = seance
        context['tickets_sold_out'] = tickets_sold_out

    return render(request, 'movies/movie_details.html', context)

def buy_ticket_view(request, *args, **kwargs):
    """
    Choose a seats and create a ticket
    """
    context = {}
    user = request.user

    if request.method == 'GET':
        # Get seance id from url
        seance_id = kwargs.get('seance_id')
        # Get seance object with given id
        seance = ProgramModel.objects.get(id=seance_id)
        try:
            # Get taken seats for the seance
            seats = SeatsModel.objects.filter(program=seance)
            taken_seats = ''
            for seat_number in seats:
                taken_seats += seat_number.seats_numbers + ','
        except SeatsModel.DoesNotExist:
            taken_seats = ''

        # Get seats reserved by authenticated user
        try:
            # Get ticket for given seance and user
            tickets = TicketsModel.objects.filter(program=seance, user=user)
            # Append seats reserved by user
            reserved_seats = ''
            for ticket in tickets:
                reserved_seats += ticket.seats.seats_numbers + ','
        except TicketsModel.DoesNotExist:
            reserved_seats = ''


        context['seance'] = seance
        context['taken_seats'] = taken_seats[0:-1]
        context['reserved_seats'] = reserved_seats[0:-1]

    return render(request, 'movies/buy_ticket.html', context)

def create_ticket_view(request):
    """
    Create a ticket after user buy it
    """
    payload = {}
    user = request.user

    if request.method == 'POST' and user.is_authenticated:
        # Get data from request
        program_id = request.POST.get('program_id')
        seats = request.POST.get('seats')
        print(program_id)
        print(seats)
        # Check if program with given id exist
        try:
            program = ProgramModel.objects.get(id=int(program_id))

            # Check if given seats are avialable
            try:
                for seat in seats.split(','):
                    # If seat is already occupied
                    s = SeatsModel.objects.get(seats_numbers__contains=seat)
                    if len(seats.split(',')) > 1:
                        payload['response'] = 'One of the selected seats is already occupied.'
                    else:
                        payload['response'] = 'This place is already taken.'
            except SeatsModel.DoesNotExist:
                # Seats are avialble
                try:
                    # Check if the user has already booked seats for this seance, if so, add new seats to the existing ticket
                    ticket = TicketsModel.objects.get(program=program, user=user)
                    # Get the seats object for given seanse
                    users_seats = SeatsModel.objects.get(id=ticket.seats.id)
                    # Add new seats to the seats object
                    new_seats = str(users_seats) + ',' + seats
                    users_seats.seats_numbers = new_seats
                    users_seats.save()
                except TicketsModel.DoesNotExist:
                    # Create seats object
                    reserved_seats = SeatsModel.objects.create(program=program, seats_numbers=seats)
                    # Create ticket
                    TicketsModel.objects.create(program=program, user=user, seats=reserved_seats)
                    payload['response'] = 'Ticket created.'
        except ProgramModel.DoesNotExist:
            payload['response'] = 'Given seance does not exist!'
    else:
        payload['response'] = 'You must be authenticated to buy a ticket.'
    
    return HttpResponse(json.dumps(payload))

def tickets_view(request):
    """
    View all tickets of authenticated user
    """
    context = {}
    user = request.user

    if request.method == 'GET':
        user_tickets = TicketsModel.objects.filter(user=user)
        tickets = []
        # Combine tickets with information about refund
        for ticket in user_tickets:
            tickets.append((ticket, check_if_refundable(ticket.id)))

        context['tickets'] = tickets
    
    return render(request, 'movies/tickets.html', context)

def return_ticket_view(request):
    """
    Return the ticket
    """
    paylod = {}
    user = request.user

    if request.method == 'POST' and user.is_authenticated:
        # Get ticket id from request
        ticket_id = request.POST.get('ticket_id')
        try:
            ticket = TicketsModel.objects.get(id=int(ticket_id))
            # Confirm that the ticket belong to authenticated user
            if ticket.user == user:
                # Check if ticket is refundable
                if check_if_refundable(ticket_id):
                    # Delete seats and ticket
                    seats = SeatsModel.objects.get(id=ticket.seats.id)
                    seats.delete()
                    ticket.delete()
                    paylod['response'] = 'Ticket returned.'
                else:
                    paylod['response'] = 'You cannot return this ticket.'
            else:
                paylod['response'] = "You cannot return someone else's ticket."
        except TicketsModel.DoesNotExist:
            paylod['response'] = 'Ticket does not exist.'
    else:
        paylod['response'] = 'You must be authenticated to return ticket.'
    
    return HttpResponse(json.dumps(paylod))

def load_qr_code_view(request, *args, **kwargs):
    """
    Create qr code and show it to user
    """
    context = {}
    user = request.user

    if request.method == 'GET':
        ticket_id = kwargs.get('ticket_id')
        # Check if ticket with given id exist
        try:
            ticket = TicketsModel.objects.get(id=ticket_id)
            # Check if the ticket belongs to authenticated user
            if ticket.user == user:
                qr_code_info = f'{ticket.id}/{ticket.program.id}/{ticket.user.id}'
                context['qr_code_info'] = qr_code_info
            else:
                raise ValueError('This ticket does not belong to you')

        except TicketsModel.DoesNotExist:
            raise ValueError('This ticket does not exist.')
    
    return render(request, 'movies/qr_code.html', context)