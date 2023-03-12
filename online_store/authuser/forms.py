from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from authuser.models import User


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
