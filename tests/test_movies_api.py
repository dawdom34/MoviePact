from datetime import datetime, timedelta

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from django.urls import reverse

from users.models import UserModel

from movies.models import MovieModel, ProgramModel, SeatsModel, TicketsModel


class TestMoviesAPI(APITestCase):

    def setUp(self):
        # Create users
        self.user = UserModel.objects.create_user(email='exampleemail@gmail.com', password='ValidP@$$w0rd')
        self.user2 = UserModel.objects.create_user(email='examplenewemail@gmail.com', password='ValidP@$$w0rd')
        # Create Movie and session
        self.movie = MovieModel.objects.create(title='Title', description='DESC', trailer_link='https://www.youtube.com',
                                               category='Movie', duration=120, age_category=12, cast='cast', release_date='2023-02-01',
                                               direction='Mark', script='Mark')
        self.program = ProgramModel.objects.create(movie=self.movie, date=datetime.now(), price=12.00)
        # Create ticket and seats
        self.seats = SeatsModel.objects.create(program=self.program, seats_numbers='1-1,1-2')
        self.ticket = TicketsModel.objects.create(program=self.program, user=self.user, seats=self.seats)
        return super().setUp()
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def test_home_200(self):
        home_url = reverse('movies_api:home')
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_home_400(self):
        self.program.date = datetime.now() + timedelta(days=1)
        self.program.save()
        home_url = reverse('movies_api:home')
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_date_filter_200(self):
        date_filter_url = reverse('movies_api:date_filter')
        data = {
            'date': datetime.now().date()
        }
        response = self.client.post(date_filter_url, data=data)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_date_filter_400(self):
        date_filter_url = reverse('movies_api:date_filter')
        data = {
            'date': '2023-14-22'
        }
        response = self.client.post(date_filter_url, data)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_movie_details_200(self):
        movie_details_url = reverse('movies_api:details', kwargs={'seance_id': self.program.id})
        response = self.client.get(movie_details_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movie_details_200_tickets_sold_out(self):
        # Create 46 seats
        SeatsModel.objects.create(program=self.program, seats_numbers=','.join([str(x) for x in range(46)]))
        movie_details_url = reverse('movies_api:details', kwargs={'seance_id': self.program.id})
        response = self.client.get(movie_details_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movie_details_400(self):
        movie_details_url = reverse('movies_api:details', kwargs={'seance_id': 123})
        response = self.client.get(movie_details_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_buy_ticket_200(self):
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        buy_ticket_url = reverse('movies_api:buy_ticket', kwargs={'seance_id': self.program.id})
        response = client.get(buy_ticket_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_buy_ticket_400(self):
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        buy_ticket_url = reverse('movies_api:buy_ticket', kwargs={'seance_id': 123})
        response = client.get(buy_ticket_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_ticket_200(self):
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        create_ticket_url = reverse('movies_api:create_ticket')
        data = {
            'program_id': self.program.id,
            'seats': '1-3,1-4'
        }
        response = client.post(create_ticket_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_ticket_200_new_ticket(self):
        token = self.get_tokens_for_user(self.user2)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        create_ticket_url = reverse('movies_api:create_ticket')
        data = {
            'program_id': self.program.id,
            'seats': '1-5,1-6'
        }
        response = client.post(create_ticket_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_ticket_400_invalid_program_id(self):
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        create_ticket_url = reverse('movies_api:create_ticket')
        data = {
            'program_id': 123,
            'seats': '2-3'
        }
        response = client.post(create_ticket_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_ticket_400_invalid_seats(self):
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        create_ticket_url = reverse('movies_api:create_ticket')
        data = {
            'program_id': self.program.id,
            'seats': '1-1,1-2'
        }
        response = client.post(create_ticket_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_ticket_400_invalid_seat(self):
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        create_ticket_url = reverse('movies_api:create_ticket')
        data = {
            'program_id': self.program.id,
            'seats': '1-1'
        }
        response = client.post(create_ticket_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_ticket_400_invalid_seats(self):
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        create_ticket_url = reverse('movies_api:create_ticket')
        data = {
            'program_id': self.program.id,
            'seats': '1-1,1-2'
        }
        response = client.post(create_ticket_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tickets_view_200(self):
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        tickets_view_url = reverse('movies_api:my_tickets')
        response = client.get(tickets_view_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_ticket_200(self):
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        return_ticket_url = reverse('movies_api:return_ticket')
        data = {
            'ticket_id': self.ticket.id
        }
        # add 24h to session to be returnable
        self.program.date = datetime.now() + timedelta(days=1)
        self.program.save()
        response = client.post(return_ticket_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_ticket_400_invalid_ticket_id(self):
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        return_ticket_url = reverse('movies_api:return_ticket')
        data = {
            'ticket_id': 123
        }
        # add 24h to session to be returnable
        self.program.data = datetime.now() + timedelta(days=1)
        self.program.save()
        response = client.post(return_ticket_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_ticket_400_wrong_user(self):
        token = self.get_tokens_for_user(self.user2)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        return_ticket_url = reverse('movies_api:return_ticket')
        data = {
            'ticket_id': self.ticket.id
        }
        # add 24h to session to be returnable
        self.program.data = datetime.now() + timedelta(days=1)
        self.program.save()
        response = client.post(return_ticket_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_ticket_400_not_refundable(self):
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        return_ticket_url = reverse('movies_api:return_ticket')
        data = {
            'ticket_id': self.ticket.id
        }
        response = client.post(return_ticket_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_load_qr_code_200(self):
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        load_code_url = reverse('movies_api:qr_code', kwargs={'ticket_id': self.ticket.id})
        response = client.get(load_code_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_load_qr_code_400_wrong_user(self):
        token = self.get_tokens_for_user(self.user2)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        load_code_url = reverse('movies_api:qr_code', kwargs={'ticket_id': self.ticket.id})
        response = client.get(load_code_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_load_qr_code_400_ivnalid_ticket_id(self):
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        load_code_url = reverse('movies_api:qr_code', kwargs={'ticket_id': 123})
        response = client.get(load_code_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
