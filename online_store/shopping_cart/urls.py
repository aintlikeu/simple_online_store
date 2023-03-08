from django.urls import path
from . import views

app_name = 'shopping_cart'

urlpatterns = [
    path('cart/', views.show_cart, name='show_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
