from django.urls import path
from .views import( HomePageAPIView, 
                   DateFilterAPIView, 
                   MovieDetailsAPIView, 
                   BuyTicketAPIView, 
                   CreateTicketAPIView,
                   TicketsAPIView,
                   ReturnTicketAPIVIew,
                   LoadQRCodeAPIView)

app_name = 'movies_api'

urlpatterns = [
    # Home page (movie sessions for today's date)
    path('home/', HomePageAPIView.as_view(),  name='home'),
    # Filter movies by date
    path('date_filter/', DateFilterAPIView.as_view(), name='date_filter'),
    # Seance details
    path('details/<int:seance_id>/', MovieDetailsAPIView.as_view(), name='details'),
    # Buy ticket
    path('ticket/<int:seance_id>/',  BuyTicketAPIView.as_view(), name='buy_ticket'),
    # Create ticket
    path('ticket/create/', CreateTicketAPIView.as_view(), name='create_ticket'),
    # User tickets
    path('my_tickets/', TicketsAPIView.as_view(), name='my_tickets'),
    # Return Ticket
    path('ticket/return/', ReturnTicketAPIVIew.as_view(), name='return_ticket'),
    # Load ticket QR code
    path('ticket/<int:ticket_id>/qr_code/', LoadQRCodeAPIView.as_view(), name='qr_code')
]