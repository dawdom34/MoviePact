from django.test import TestCase
from django.urls import reverse

from users.models import UserModel
from users.forms import AccountRegisterForm


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(email='takenemail@gmail.com', password='validPassword1234')
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        return super().setUp()
    

class UsersRegisterTest(BaseTest):
    def test_user_register_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_user_register_post_invalid(self):
        invalid_data = {'email': '', 'password1': 'p@$$w0rd', 'password2': 'p@$$w0rd'}
        response = self.client.post(self.register_url, data=invalid_data, format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_user_register_errors(self):
        with self.assertRaisesMessage(ValueError, 'Users must have an email address.'):
            UserModel.objects.create_user(email='', password='validPassword1234')

    def test_user_register_post_valid(self):
        valid_data = {'email': 'validemail@gmail.com', 'password1': 'validPassword123', 'password2': 'validPassword123'}
        response = self.client.post(self.register_url, data=valid_data, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_user_register_post_with_email_already_in_use(self):
        data = {'email': 'takenemail@gmail.com', 'password1': 'validPassword123', 'password2': 'validPassword123'}
        response = self.client.post(self.register_url, data=data, format='text/html')
        self.assertEqual(response.status_code, 200)
        form = AccountRegisterForm(data)
        self.assertEqual(form.errors, {'email': ['Email takenemail@gmail.com is already in use!']})

    def test_user_register_get_when_user_already_authenticated(self):
        data = {'email': 'takenemail@gmail.com', 'password': 'validPassword1234'}
        self.client.post(self.login_url, data=data)
        response = self.client.get(self.register_url)
        self.assertEqual(response.content, b'You are already authenticated as takenemail@gmail.com.')



class UsersLoginTest(BaseTest):
    def test_user_login_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_user_login_post_invalid(self):
        data = {'email': 'invalidemail@gmail.com', 'password': 'randompassword'}
        response = self.client.post(self.login_url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_user_login_post_valid(self):
        data = {'email': 'takenemail@gmail.com', 'password': 'validPassword1234'}
        response = self.client.post(self.login_url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_user_login_get_when_user_already_authenticated(self):
        data = {'email': 'takenemail@gmail.com', 'password': 'validPassword1234'}
        self.client.post(self.login_url, data=data)
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        data = {'email': 'takenemail@gmail.com', 'password': 'validPassword1234'}
        self.client.post(self.login_url, data=data)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)


class CreateSuperUser(BaseTest):
    def test_create_super_user(self):
        user = UserModel.objects.create_superuser(email='superuser123@gmail.com', password='superpassword1234')
        self.assertEqual(str(user), 'superuser123@gmail.com')
        self.assertEqual(user.has_perm('perm'), True)
        self.assertEqual(user.has_module_perms('app_label'), True)
