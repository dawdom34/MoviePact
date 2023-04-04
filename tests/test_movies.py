from django.test import TestCase
from django.urls import reverse

from datetime import datetime, timedelta

from users.models import UserModel
from movies.forms import MovieCreationForm, ProgramCreationForm
from movies.models import MovieModel, ProgramModel, SeatsModel, TicketsModel


class BaseTest(TestCase):
    def setUp(self):
        # Create superuser
        self.super_user = UserModel.objects.create_superuser(email='examplenewemail@gmail.com', password='ValidP@$$word')
        # Create user
        self.user = UserModel.objects.create_user(email='exampleemail@gmail.com', password='ValidP@$$word')
        # Authentication data
        self.auth_superuser_data = {'email': 'examplenewemail@gmail.com', 'password': 'ValidP@$$word'}
        self.auth_user_data = {'email': 'exampleemail@gmail.com', 'password': 'ValidP@$$word'}
        # Create movie
        self.movie = MovieModel.objects.create(title='title', description='desc', trailer_link='https://www.youtube.com', category='drama', duration=123,
                                               age_category=12, cast='cast', release_date=datetime.now().date(), direction='dir', script='sc')
        # Create seance
        self.seance = ProgramModel.objects.create(movie=self.movie, date=datetime.now(), price=12.99)
        print(self.seance)
        
        # Ticket data
        self.ticket_data = {'program_id': self.seance.id, 'seats': '1,2,3'}

        # URLS
        self.login_url = reverse('login')
        self.create_movie_url = reverse('movies:create_movie')
        self.create_program_url = reverse('movies:create_program')
        self.home_url = reverse('home')
        self.date_filter_url = reverse('movies:filter', kwargs={'date': '2022-02-01'})
        self.movie_details_url = reverse('movies:details', kwargs={'seance_id': self.seance.id})
        self.buy_ticket_url = reverse('movies:buy_ticket', kwargs={'seance_id':  self.seance.id})
        self.create_ticket_url = reverse('movies:create_ticket')
        self.tickets_url = reverse('movies:tickets')
        self.return_ticket_url = reverse('movies:return_ticket')
        
        return super().setUp()
    

class MoviesTest(BaseTest):
    def test_create_movie_user_not_authenticated(self):
        response = self.client.get(self.create_movie_url)
        self.assertEqual(response.status_code, 302)

    def test_create_movie_user_without_privileges(self):
        # Login user
        self.client.post(self.login_url, self.auth_user_data)
        response = self.client.get(self.create_movie_url)
        self.assertEqual(response.content, b'Access denied!')

    def test_create_movie_get(self):
        # Login user with privileges
        self.client.post(self.login_url, self.auth_superuser_data)
        response = self.client.get(self.create_movie_url)
        self.assertEqual(response.status_code, 200)

    def test_create_movie_post_valid(self):
        # Login user with privileges
        self.client.post(self.login_url, self.auth_superuser_data)
        # Movie data
        self.movie_data = {'title': 'ExampleTitle', 'description': 'ExampleDescription', 'trailer_link': 'https://www.youtube.com', 'category': 'category', 'duration': 123, 'age_category': 12,
                           'cast': 'cast', 'release_date': datetime.now().date(), 'direction': 'dir', 'script': 'script'}
        form = MovieCreationForm(self.movie_data)
        self.assertEqual(form.is_valid(), True)
        self.assertEqual(form.errors, {})
        response = self.client.post(self.create_movie_url, self.movie_data)
        self.assertEqual(response.status_code, 302)
        movie = MovieModel.objects.get(title='ExampleTitle')
        self.assertIsInstance(movie, MovieModel)

    def test_create_movie_post_invalid(self):
        data = {'title': 'title', 'description': 'ExampleDescription', 'trailer_link': 'https://www.youtube.com', 'category': 'category', 'duration': 123, 'age_category': 12,
                           'cast': 'cast', 'release_date': datetime.now().date(), 'direction': 'dir', 'script': 'script'}
        self.client.post(self.create_movie_url, data)
        response = self.client.post(self.create_movie_url)
        m = MovieModel.objects.get(title='title')
        self.assertIsInstance(m, MovieModel)
        self.assertEqual(response.status_code, 200)
        

    def test_create_movie_form_invalid(self):
        data = {'title': 'title', 'description': 'ExampleDescription', 'trailer_link': 'https://www.youtube.com', 'category': 'category', 'duration': 123, 'age_category': 12,
                           'cast': 'cast', 'release_date': datetime.now().date(), 'direction': 'dir', 'script': 'script'}
        form = MovieCreationForm(data)
        self.assertEqual(form.errors, {'title': ['Movie with title "title" already exist!']})
        

    def test_create_program_view_when_user_not_auth(self):
        response = self.client.get(self.create_program_url)
        self.assertEqual(response.status_code, 302)

    def test_create_program_view_when_user_not_staff(self):
        # Login user
        self.client.post(self.login_url, self.auth_user_data)
        response = self.client.get(self.create_program_url)
        self.assertEqual(response.content, b'Access denied!')

    def test_create_program_view_get(self):
        self.client.post(self.login_url, self.auth_superuser_data)
        response = self.client.get(self.create_program_url)
        self.assertEqual(response.status_code, 200)

    def test_create_program_view_post_valid(self):
        self.client.post(self.login_url, self.auth_superuser_data)
        data = {'movie': self.movie.id, 'date': datetime(2023, 2, 1), 'price': 12.99}
        response = self.client.post(self.create_program_url, data)
        self.assertEqual(response.status_code, 302)

    def test_create_program_view_post_invalid(self):
        self.client.post(self.login_url, self.auth_superuser_data)
        data = {'movie': self.movie.id, 'date': datetime(2023, 2, 1), 'price': 12.99}
        self.client.post(self.create_program_url, data)
        response = self.client.post(self.create_program_url, data)
        self.assertEqual(response.status_code, 200)

    def test_home_view_get(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_date_filter_view_get(self):
        response = self.client.get(self.date_filter_url)
        self.assertEqual(response.status_code, 200)

    def test_movie_details_view_get(self):
        # Create some seats
        SeatsModel.objects.create(program=self.seance, seats_numbers='1,2')
        response = self.client.get(self.movie_details_url)
        self.assertEqual(response.status_code, 200)

    def test_movie_details_view_get_invalid_id(self):
        invalid_url = reverse('movies:details', kwargs={'seance_id': 123})
        response = self.client.get(invalid_url)
        self.assertEqual(response.content, b'Seance with given id does not exist.')
    
    def test_movie_details_view_get_tickets_out(self):
        # Create 48 seats objects
        SeatsModel.objects.create(program=self.seance, seats_numbers=','.join([str(x) for x in range(48)]))
        response = self.client.get(self.movie_details_url)
        self.assertEqual(response.status_code, 200)

    def test_buy_ticket_view_get(self):
        # Login user
        self.client.post(self.login_url, self.auth_user_data)
        # Create reserved seats
        SeatsModel.objects.create(program=self.seance, seats_numbers='1,2')
        # Create seats reserved by auth user
        seats = SeatsModel.objects.create(program=self.seance, seats_numbers='3,4')
        TicketsModel.objects.create(program=self.seance, user=self.user, seats=seats)
        response = self.client.get(self.buy_ticket_url)
        self.assertEqual(response.status_code, 200)

    def test_buy_ticket_view_get_with_invalid_seance_id(self):
        # Login user
        self.client.post(self.login_url, self.auth_user_data)
        invalid_url = reverse('movies:buy_ticket', kwargs={'seance_id': 123})
        response = self.client.get(invalid_url)
        self.assertEqual(response.content, b'Seance with given id does not exist.')

    def test_create_ticket_view_user_not_auth(self):
        response = self.client.post(self.create_ticket_url, self.ticket_data, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.content, b'{"response": "You must be authenticated to buy a ticket."}')

    def test_create_ticket_view_with_invalid_seance_id(self):
        # Login user
        self.client.post(self.login_url, self.auth_user_data)
        invalid_ticket_data = {'program_id': 1233, 'seats': '1,2,3'}
        response = self.client.post(self.create_ticket_url, invalid_ticket_data, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.content, b'{"response": "Given seance does not exist!"}')
    
    def test_create_ticket_view_with_multiple_seats_already_occupied(self):
        # Create reserved seats
        SeatsModel.objects.create(program=self.seance, seats_numbers='1,2')
        # Login user
        self.client.post(self.login_url, self.auth_user_data)
        invalid_ticket_data = {'program_id': self.seance.id, 'seats': '1,2'}
        response = self.client.post(self.create_ticket_url, invalid_ticket_data, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.content, b'{"response": "One of the selected seats is already occupied."}')

    def test_create_ticket_view_with_one_place_already_occupied(self):
        # Create reserved seats
        SeatsModel.objects.create(program=self.seance, seats_numbers='1')
        # Login user
        self.client.post(self.login_url, self.auth_user_data)
        invalid_ticket_data = {'program_id': self.seance.id, 'seats': '1'}
        response = self.client.post(self.create_ticket_url, invalid_ticket_data, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.content, b'{"response": "This place is already taken."}')

    def test_create_ticket_view_with_seats_already_booked(self):
        # Login user
        self.client.post(self.login_url, self.auth_user_data)
        valid_ticket_data = {'program_id': self.seance.id, 'seats': '4,5'}
        self.client.post(self.create_ticket_url, self.ticket_data, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        response = self.client.post(self.create_ticket_url, valid_ticket_data, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.content, b'{"response": "Ticket created."}')

    def test_create_ticket_view(self):
        # Login user
        self.client.post(self.login_url, self.auth_user_data)
        response = self.client.post(self.create_ticket_url, self.ticket_data, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.content, b'{"response": "Ticket created."}')

    def test_tickets_view_when_user_not_auth(self):
        response = self.client.get(self.tickets_url)
        self.assertEqual(response.status_code, 302)

    def test_tickets_view_get(self):
        # Login user
        self.client.post(self.login_url, self.auth_user_data)
        # Create reserved seats
        seats = SeatsModel.objects.create(program=self.seance, seats_numbers='3,4')
        # Create ticket
        TicketsModel.objects.create(program=self.seance, user=self.user, seats=seats)
        response = self.client.get(self.tickets_url)
        self.assertEqual(response.status_code, 200)

    def test_return_ticket_user_not_auth(self):
        response = self.client.post(self.return_ticket_url)
        self.assertEqual(response.content, b'{"response": "You must be authenticated to return ticket."}')

    def test_return_ticket_view_with_invalid_ticket_id(self):
        # Login user
        self.client.post(self.login_url, self.auth_user_data)
        invalid_ticket_data = {'ticket_id': 123}
        response = self.client.post(self.return_ticket_url, invalid_ticket_data, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.content, b'{"response": "Ticket does not exist."}')

    def test_return_ticket_view_when_user_does_not_own_the_ticket(self):
        # Login user
        self.client.post(self.login_url, self.auth_superuser_data)
        # Create reserved seats
        seats = SeatsModel.objects.create(program=self.seance, seats_numbers='3,4')
        # Create ticket
        ticket = TicketsModel.objects.create(program=self.seance, user=self.user, seats=seats)
        ticket_data = {'ticket_id': ticket.id}
        response = self.client.post(self.return_ticket_url, ticket_data, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.content, b'{"response": "Error while returning the ticket."}')

    def test_return_ticket_view_when_ticket_not_returnable(self):
        # Login user
        self.client.post(self.login_url, self.auth_user_data)
        # Create reserved seats
        seats = SeatsModel.objects.create(program=self.seance, seats_numbers='3,4')
        # Create ticket
        ticket = TicketsModel.objects.create(program=self.seance, user=self.user, seats=seats)
        ticket_data = {'ticket_id': ticket.id}
        response = self.client.post(self.return_ticket_url, ticket_data, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.content, b'{"response": "You cannot return this ticket."}')

    def test_return_ticket_view(self):
        # Login user
        self.client.post(self.login_url, self.auth_user_data)
        # Create new seance with a difference of 12 hours
        twelwe_hours_from_now = datetime.now() + timedelta(hours=12)
        seance = ProgramModel.objects.create(movie=self.movie, date=twelwe_hours_from_now, price=12.00)
        # Create reserved seats
        seats = SeatsModel.objects.create(program=seance, seats_numbers='3,4')
        # Create ticket
        ticket = TicketsModel.objects.create(program=seance, user=self.user, seats=seats)
        ticket_data = {'ticket_id': ticket.id}
        response = self.client.post(self.return_ticket_url, ticket_data, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.content, b'{"response": "Ticket returned."}')

    def test_load_qr_code_view_user_not_auth(self):
        qr_code_url = reverse('movies:qr_code', kwargs={'ticket_id': 1})
        response = self.client.get(qr_code_url)
        self.assertEqual(response.status_code, 302)

    def test_load_qr_code_with_invalid_ticket_id(self):
        # Login user
        self.client.post(self.login_url, self.auth_user_data)
        qr_code_url = reverse('movies:qr_code', kwargs={'ticket_id': 1})
        response = self.client.get(qr_code_url)
        self.assertEqual(response.content, b'This ticket does not exist.')

    def test_load_qr_code_with_ticket_user_does_not_own(self):
        # Login user
        self.client.post(self.login_url, self.auth_superuser_data)
        # Create reserved seats
        seats = SeatsModel.objects.create(program=self.seance, seats_numbers='3,4')
        # Create ticket
        ticket = TicketsModel.objects.create(program=self.seance, user=self.user, seats=seats)
        qr_code_url = reverse('movies:qr_code', kwargs={'ticket_id': ticket.id})
        response = self.client.get(qr_code_url)
        self.assertEqual(response.content, b'Error while loading QR code.')

    def test_load_qr_code_valid(self):
        # Login user
        self.client.post(self.login_url, self.auth_user_data)
        # Create reserved seats
        seats = SeatsModel.objects.create(program=self.seance, seats_numbers='3,4')
        # Create ticket
        ticket = TicketsModel.objects.create(program=self.seance, user=self.user, seats=seats)
        qr_code_url = reverse('movies:qr_code', kwargs={'ticket_id': ticket.id})
        response = self.client.get(qr_code_url)
        self.assertEqual(response.status_code, 200)