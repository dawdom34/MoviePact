from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.urls import reverse

from users.models import UserModel
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class RegisterTest(APITestCase):
    def test_register_api_200(self):
        data = {
            'email': 'exampleemail@gmail.com',
            'password': 'validP@$$w0rd123',
            'password2': 'validP@$$w0rd123'
        }
        register_url = reverse('users_api:register')
        response = self.client.post(register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_400(self):
        data = {
            'email': '',
            'password': 'validP@$$w0rd123',
            'password2': 'validP@$$w0rd123'
        }
        register_url = reverse('users_api:register')
        response = self.client.post(register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_password_does_not_match(self):
        data = {
            'email': 'exampleemail@gmail.com',
            'password': 'validP@$$w0rd123',
            'password2': 'validP@$$w0rd12345'
        }
        register_url = reverse('users_api:register')
        response = self.client.post(register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginLogoutTest(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='exampleemail@gmail.com', password='validP@$$w0rd123')

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
    
    def test_login_success(self):
        data = {
            'email': 'exampleemail@gmail.com',
            'password': 'validP@$$w0rd123'
        }
        login_url = reverse('users_api:login')
        response = self.client.post(login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_400(self):
        data = {
            'email': 'exampleemail',
            'password': 'validP@$$w0rd123'
        }
        login_url = reverse('users_api:login')
        response = self.client.post(login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_does_not_exist(self):
        data = {
            'email': 'invalidemail@gmail.com',
            'password': 'validP@$$w0rd123'
        }
        login_url = reverse('users_api:login')
        response = self.client.post(login_url, data)
        self.assertEqual(response.content, b'{"errors":{"non field errors":["Email or Password is not valid"]}}')

    def test_login_user_with_invalid_password(self):
        data = {
            'email': 'exampleemail@gmail.com',
            'password': 'invalidP@$$w0rd123'
        }
        login_url = reverse('users_api:login')
        response = self.client.post(login_url, data)
        self.assertEqual(response.content, b'{"errors":{"non field errors":["Email or Password is not valid"]}}')
        
    def test_logout_user(self):
        logout_url = reverse('users_api:logout')
        user = UserModel.objects.get(email='exampleemail@gmail.com')
        token = self.get_tokens_for_user(user)
        data = {'refresh_token': token['refresh']}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        response = client.post(logout_url, data)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)


class TestUserProfileView(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='exampleemail@gmail.com', password='validP@$$w0rd123')
        return super().setUp()
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def test_user_profile_view(self):
        profile_view_url = reverse('users_api:profile')
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        response = client.get(profile_view_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestChangePassword(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='exampleemail@gmail.com', password='validP@$$w0rd123')
        return super().setUp()
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def test_change_password_200(self):
        change_password_url = reverse('users_api:change_password')
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        data = {
            "password": 'zaq1poiuy',
            "password2": 'zaq1poiuy'
        }
        response = client.post(change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_400(self):
        change_password_url = reverse('users_api:change_password')
        token = self.get_tokens_for_user(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        data = {
            "password": 'zaq1poiuy',
            "password2": 'zaq1poiuy123'
        }
        response = client.post(change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestPasswordReset(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='exampleemail@gmail.com', password='validP@$$w0rd123')
        return super().setUp()
    
    def test_send_password_reset_email_400(self):
        reset_password_url = reverse('users_api:send-reset-password-email')
        data = {
            "email": "invalidemail@gmail.com"
        }
        response = self.client.post(reset_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_reset_email_200(self):
        reset_password_url = reverse('users_api:send-reset-password-email')
        data = {
            "email": "exampleemail@gmail.com"
        }
        response = self.client.post(reset_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_400(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.id))
        token = PasswordResetTokenGenerator().make_token(self.user)
        password_reset_url =  reverse('users_api:reset-password',  kwargs={'uid': uid, 'token': token})
        data = {
            "password": 'zaq1poiuy',
            "password2": 'zaq1wert'
        }
        response= self.client.post(password_reset_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_200(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.id))
        token = PasswordResetTokenGenerator().make_token(self.user)
        password_reset_url =  reverse('users_api:reset-password',  kwargs={'uid': uid, 'token': token})
        data = {
            "password": 'zaq1poiuy',
            "password2": 'zaq1poiuy'
        }
        response= self.client.post(password_reset_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_invalid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.id))
        token = 'invalidtoken123'
        password_reset_url =  reverse('users_api:reset-password',  kwargs={'uid': uid, 'token': token})
        data = {
            "password": 'zaq1poiuy',
            "password2": 'zaq1poiuy'
        }
        response= self.client.post(password_reset_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)