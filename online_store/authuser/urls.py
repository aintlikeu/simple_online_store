from django.urls import path
from . import views

app_name = 'authuser'

urlpatterns = [
    path('', views.example_view)
]