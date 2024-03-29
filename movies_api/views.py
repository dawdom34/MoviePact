from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.forms.models import model_to_dict

from datetime import datetime, timedelta

from movies.models import ProgramModel, SeatsModel, TicketsModel
from movies.utils import check_if_refundable

from .serializers import DateFilterSerializer, CreateTicketSerializer, ReturnTicketSerializer


class HomePageAPIView(APIView):
    """
    Get todays movie sessions
    """
    def get(self, request):
        today = datetime.now().strftime(r'%Y-%m-%d')
        program = ProgramModel.objects.filter(date__date = today)
        data = {}
        if program:
            for x in program:
                title = x.movie.title
                duration = x.movie.duration
                age_category = x.movie.age_category
                data[x.id] = {'id': x.id, 'title': title, 'duration': duration, 'price': x.price, 'age_category': age_category}
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class DateFilterAPIView(APIView):
    """
    Get movie sessions for selected day
    """
    def post(self, request):
        serializer = DateFilterSerializer(data=request.data)
        if serializer.is_valid():
            data = {}
            date = serializer.data['date']
            # Todays date
            today = (datetime.now().strftime(r'%m-%d'), datetime.now().strftime(r'%A'), datetime.now().strftime(r'%Y-%m-%d'))
            days = []
            # Dates for next 14 days
            for x in range(1,14):
                next = datetime.now() + timedelta(days=x)
                days.append((next.strftime(r'%m-%d'), next.strftime(r'%A'), next.strftime(r'%Y-%m-%d')))
            # Get the movies from selected date
            selected_date = datetime(year=int(date[0:4]), month=int(date[5:7]), day=int(date[8:])).date()
            program = ProgramModel.objects.filter(date__date=date)
            program_data = {}
            if program:
                for x in program:
                    title = x.movie.title
                    duration = x.movie.duration
                    age_category = x.movie.age_category
                    program_data[x.id] = {'id': x.id, 'title': title, 'duration': duration, 'price': x.price, 'age_category': age_category}

            data['today'] = today
            data['days'] = days
            data['selected_date'] = selected_date
            data['program'] = program_data
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MovieDetailsAPIView(APIView):
    """
    Get seance details and information about vacanties
    """
    def get(self, request, **kwargs):
        # Get seance with given id
        seance_id = kwargs.get('seance_id')
        try:
            seance = ProgramModel.objects.get(id=seance_id)
            # Seance details
            seance_details = {}
            seance_details['id'] = seance.id
            seance_details['title'] = seance.movie.title
            seance_details['description'] = seance.movie.description
            seance_details['category'] = seance.movie.category
            seance_details['duration'] = seance.movie.duration
            seance_details['age_category'] = seance.movie.age_category
            seance_details['premiere'] = seance.movie.release_date
            seance_details['cast'] = seance.movie.cast
            seance_details['direction'] = seance.movie.direction
            seance_details['script'] = seance.movie.script
            seance_details['price'] = seance.price
            seance_details['poster'] = seance.movie.poster.url

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

            seance_details['tickets_sold_out'] = tickets_sold_out

            return Response(seance_details, status=status.HTTP_200_OK)
        except ProgramModel.DoesNotExist:
            return Response({'error': 'Seance with given id does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        

class BuyTicketAPIView(APIView):
    """
    Choose a seats and create a ticket
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        seance_id = kwargs.get('seance_id')
        user = request.user
        try:
            data = {}
            seance = ProgramModel.objects.get(id=seance_id)
            # Get taken seats for the seance
            seats = SeatsModel.objects.filter(program=seance)
            taken_seats = ''
            if len(seats) > 0:
                for seat_number in seats:
                    taken_seats += seat_number.seats_numbers + ','
            

            # Get seats reserved by authenticated user
            tickets = TicketsModel.objects.filter(program=seance, user=user)
            reserved_seats = ''
            if len(tickets)  > 0:
                # Append seats reserved by user
                for ticket in tickets:
                    reserved_seats += ticket.seats.seats_numbers + ','
            
            data['title'] = seance.movie.title
            data['date'] = seance.date
            data['taken_seats'] = taken_seats
            data['reserved_seats'] = reserved_seats

            return Response(data, status=status.HTTP_200_OK)
        except ProgramModel.DoesNotExist:
            return Response({'error': 'Seance with given id does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        

class CreateTicketAPIView(APIView):
    """
    Create a ticket after user buy it
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateTicketSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            return Response({'msg': 'Ticket created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TicketsAPIView(APIView):
    """
    View all tickets of authenticated user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Get all tickets of authenticated user whose show date is greater or equal today
        user_tickets = TicketsModel.objects.filter(user=user, program__date__date__gte=datetime.now().date())
        data = {}
        for ticket in user_tickets:
            temp = {}
            temp['id'] = ticket.id
            temp['title'] = ticket.program.movie.title
            temp['date'] = ticket.program.date
            temp['poster'] = ticket.program.movie.poster.url
            temp['seats'] = ticket.seats.seats_numbers
            temp['refundable'] = check_if_refundable(ticket.id)
            data[ticket.id] = temp
        return Response(data, status=status.HTTP_200_OK)
        

class ReturnTicketAPIVIew(APIView):
    """
    Return the ticket if it's possible
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReturnTicketSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            return Response({'msg': 'Ticket returned'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoadQRCodeAPIView(APIView):
    """
    Returns the data needed to generate the qr code 
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        ticket_id = kwargs.get('ticket_id')
        user = request.user
        try:
            ticket = TicketsModel.objects.get(id=ticket_id)
            # Check if the ticket belongs to authenticated user
            if ticket.user == user:
                qr_code_info = f'{ticket.id}/{ticket.program.id}/{ticket.user.id}'
                data = {'qr_code_info': qr_code_info}
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Error while loading QR code.'}, status=status.HTTP_400_BAD_REQUEST)
        except TicketsModel.DoesNotExist:
            return Response({'error': 'This ticket does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
