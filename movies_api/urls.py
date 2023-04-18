from django.urls import path
from .views import( HomePageAPIView, 
                   DateFilterAPIView, 
                   MovieDetailsAPIView, 
                   BuyTicketAPIView, 
                   CreateTicketAPIView,
                   TicketsAPIView,
                   ReturnTicketAPIVIew)

app_name = 'movies_api'

urlpatterns = [
    path('home/', HomePageAPIView.as_view(),  name='home'),
    path('date_filter/', DateFilterAPIView.as_view(), name='date_filter'),
    path('details/<int:seance_id>/', MovieDetailsAPIView.as_view(), name='details'),
    path('ticket/<int:seance_id>/',  BuyTicketAPIView.as_view(), name='buy_ticket'),
    path('ticket/create/', CreateTicketAPIView.as_view(), name='create_ticket'),
    path('my_tickets/', TicketsAPIView.as_view(), name='my_tickets'),
    path('ticket/return/', ReturnTicketAPIVIew.as_view(), name='return_ticket')
]