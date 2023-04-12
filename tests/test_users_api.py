from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from users.models import UserModel


class RegisterTest(APITestCase):
    def test_register_api_success(self):
        data = {
            'email': 'exampleemail@gmail.com',
            'password': 'validP@$$w0rd123',
            'password2': 'validP@$$w0rd123'
        }
        register_url = reverse('users_api:register')
        response = self.client.post(register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_fail(self):
        data = {
            'email': '',
            'password': 'validP@$$w0rd123',
            'password2': 'validP@$$w0rd123'
        }
        register_url = reverse('users_api:register')
        response = self.client.post(register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginLogoutTest(APITestCase):
    def  setUp(self):
        self.user = UserModel.objects.create_user(email='exampleemail@gmail.com', password='validP@$$w0rd123')
        return super().setUp()
    
    def test_login_success(self):
        data = {
            'email': 'exampleemail@gmail.com',
            'password': 'validP@$$w0rd123'
        }
        login_url = reverse('users_api:login')
        response = self.client.post(login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_does_not_exist(self):
        data = {
            'email': 'invalidemail@gmail.com',
            'password': 'validP@$$w0rd123'
        }
        login_url = reverse('users_api:login')
        response = self.client.post(login_url, data)
        self.assertEqual(response.content, {'400': 'UserModel matching query does not exist.'})

    def test_login_user_with_invalid_password(self):
        data = {
            'email': 'exampleemail@gmail.com',
            'password': 'invalidP@$$w0rd123'
        }
        login_url = reverse('users_api:login')
        with self.assertRaisesMessage(ValueError, "{'message': 'Incorrect login data'}"):
            self.client.post(login_url, data)
        

    def test_login_user_with_inactive_account(self):
        user = UserModel.objects.get(email='exampleemail@gmail.com')
        user.is_active = False
        user.save()
        data = {
            'email': 'exampleemail@gmail.com',
            'password': 'validP@$$w0rd123'
        }
        login_url = reverse('users_api:login')
        response = self.client.post(login_url, data)
        self.assertEqual(response.content, {"400": "Account not active"})

    def test_logout_user(self):
        data = {
            'email': 'exampleemail@gmail.com',
            'password': 'validP@$$w0rd123'
        }
        login_url = reverse('users_api:login')
        self.client.post(login_url, data)
        logout_url = reverse('users_api:logout')
        response = self.client.get(logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)