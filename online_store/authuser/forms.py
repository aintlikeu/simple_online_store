from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from authuser.models import User


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField()
    password = forms.PasswordInput()


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)
