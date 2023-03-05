from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from users.models import UserModel


class AccountAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Incorrect email or password!')
            return self.cleaned_data


class AccountRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Add a valid email address.')

    class Meta:
        model = UserModel
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        """
        Email validation
        """
        email = self.cleaned_data['email'].lower()
        # Check if email is already in use
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email {email} is already in use!')
