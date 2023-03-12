from django.contrib import admin
from shopping_cart.models import Cart, CartItem, Order, OrderItem

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
