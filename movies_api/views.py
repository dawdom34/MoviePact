from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.forms.models import model_to_dict

from datetime import datetime, timedelta

from movies.models import ProgramModel

from .serializers import DateFilterSerializer


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
    def get(self, request):
        print(request.data)
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
