from django.urls import path
from .views import RegisterUserAPIView


app_name = 'users_api'

urlpatterns = [
  path('register',RegisterUserAPIView.as_view(), name='register'),
]