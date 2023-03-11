from django.urls import path
from . import views

app_name = 'shopping_cart'

urlpatterns = [
    path('cart/', views.show_cart, name='show_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/clear', views.clear_cart, name='clear_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('thank_you/', views.thank_you, name='thank_you')
]
