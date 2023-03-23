from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from authuser.forms import LoginUserForm, RegistrationForm


class LoginView(View):
    def post(self, request):
        form = LoginUserForm(data=request.POST)
        if not form.is_valid():
            messages.error(request, 'Something went wrong. Please try again', extra_tags='alert-danger')
            return redirect('authuser:login')

        email = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('catalog:product_list')
        else:
            messages.error(request, 'Something went wrong. Please try again', extra_tags='alert-danger')
            return redirect('authuser:login')

    def get(self, request):
        form = LoginUserForm()
        return render(request, 'authuser/login.html', context={'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You logged out', extra_tags='alert-success')
        return redirect('catalog:product_list')


class RegisterView(View):
    def post(self, request):
        form = RegistrationForm(data=request.POST)
        if not form.is_valid():
            messages.error(request, 'Something went wrong. Please try again', extra_tags='alert-danger')
            return redirect('authuser:register')

        form.save()
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        user = authenticate(request, email=email, password=password)
        login(request, user)
        messages.success(request, 'You were registered and logged in.', extra_tags='alert-success')
        return redirect('catalog:product_list')

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'authuser/register.html', context={'form': form})
