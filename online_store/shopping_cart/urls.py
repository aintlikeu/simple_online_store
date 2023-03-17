from django.urls import path
from shopping_cart import views

app_name = 'shopping_cart'

urlpatterns = [
    path('cart/', views.show_cart_view, name='show_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/clear', views.clear_cart_view, name='clear_cart'),
    path('cart/remove/<int:product_id>/', views.extract_from_cart_view, name='remove_from_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('thank_you/', views.thank_you_view, name='thank_you')
]
