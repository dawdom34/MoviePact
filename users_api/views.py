from .serializers import (RegisterSerializer, 
                          UserLoginSerializer, 
                          UserSerializer, 
                          UserChangePasswordSerializer, 
                          SendPasswordResetEmailSerializer,
                          PasswordResetSerializer)

from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#Class based view to register user
class RegisterUserAPIView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token,'msg': 'Register success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Class based view to login user
class LoginUserAPIView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                token = get_tokens_for_user(user)
                return Response({'token': token,'msg': 'Login success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non field errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Class based view to get user data
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Class based view to change users password
class UserChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            return Response({'msg': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Class based view to send reset password email
class SendPasswordResetEmailAPIView(APIView):
    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'msg': 'Password reset link send. Please check your Email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Class based view to reset users password
class PasswordResetAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data, context={'uid': kwargs.get('uid'), 'token': kwargs.get('token')})
        if serializer.is_valid():
            return Response({'msg': 'Password reset successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)