from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginUserForm, RegistrationForm


def example_view(request):
    return render(request, 'authuser/example.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('catalog:product_list')
            else:
                messages.success(request, 'Something went wrong. Please try again')
                return redirect('authuser:login')
        else:
            messages.success(request, 'Something went wrong. Please try again')
            return redirect('authuser:login')
    else:
        form = LoginUserForm()
        return render(request, 'authuser/login.html', context={'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You logged out')
    return redirect('catalog:product_list')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'You were registered and logged in.')
            return redirect('catalog:product_list')
        else:
            messages.success(request, 'Something went wrong. Please try again')
            return redirect('authuser:register')
    else:
        form = RegistrationForm()
        return render(request, 'authuser/register.html', context={'form': form})
