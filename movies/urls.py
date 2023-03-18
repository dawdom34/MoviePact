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
    path('add_movie/', create_movie_view, name='create_movie'),
    path('add_program/', create_program_view, name='create_program'),
    path('<str:date>', date_filter_view, name='filter'),
    path('details/<int:seance_id>', movie_details_view, name='details'),
    path('ticket/<int:seance_id>', buy_ticket_view, name='buy_ticket'),
    path('ticket/create', create_ticket_view, name='create_ticket'),
    path('my_tickets/', tickets_view, name='tickets'),
    path('ticket/return', return_ticket_view, name='return_ticket'),
    path('ticket/<int:ticket_id>/qr_code', load_qr_code_view, name='qr_code')
]