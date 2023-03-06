from django.urls import path
from . import views

app_name = 'authuser'

urlpatterns = [
    path('', views.example_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register')
]