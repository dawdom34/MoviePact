from django.urls import path
from .views import HomePageAPIView, DateFilterAPIView

app_name = 'movies_api'

urlpatterns = [
    path('home/', HomePageAPIView.as_view(),  name='home'),
    path('date_filter/', DateFilterAPIView.as_view(), name='date_filter')
]