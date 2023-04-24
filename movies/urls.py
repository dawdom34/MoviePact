from django.urls import path
from .views import (create_movie_view,
                    create_program_view,
                    date_filter_view,
                    movie_details_view,
                    buy_ticket_view,
                    create_ticket_view,
                    tickets_view,
                    return_ticket_view,
                    load_qr_code_view)

app_name = 'movies'

urlpatterns = [
    # Create new movie
    path('add_movie/', create_movie_view, name='create_movie'),
    # Create new movie session
    path('add_program/', create_program_view, name='create_program'),
    # Filter movies by date
    path('<str:date>', date_filter_view, name='filter'),
    # Seance details
    path('details/<int:seance_id>', movie_details_view, name='details'),
    # Buy ticket
    path('ticket/<int:seance_id>', buy_ticket_view, name='buy_ticket'),
    # Create ticket
    path('ticket/create', create_ticket_view, name='create_ticket'),
    # Users tickets
    path('my_tickets/', tickets_view, name='tickets'),
    # Return ticket
    path('ticket/return', return_ticket_view, name='return_ticket'),
    # Load ticket QR code
    path('ticket/<int:ticket_id>/qr_code', load_qr_code_view, name='qr_code')
]