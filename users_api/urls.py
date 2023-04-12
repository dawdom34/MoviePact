from django.urls import path
from .views import (RegisterUserAPIView, 
                    LoginUserAPIView, 
                    UserProfileView, 
                    UserChangePasswordAPIView,
                    SendPasswordResetEmailAPIView,
                    PasswordResetAPIView)


app_name = 'users_api'

urlpatterns = [
  path('register',RegisterUserAPIView.as_view(), name='register'),
  path('login', LoginUserAPIView.as_view(), name='login'),
  path('profile', UserProfileView.as_view(), name='profile'),
  path('change_password', UserChangePasswordAPIView.as_view(), name='change_password'),
  path('send-reset-password-email', SendPasswordResetEmailAPIView.as_view(), name='send-reset-password-email'),
  path('reset-password/<uid>/<token>/', PasswordResetAPIView.as_view(), name='reset-password')
]