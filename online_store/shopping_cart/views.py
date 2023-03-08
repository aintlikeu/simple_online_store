from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from catalog.models import Product


def show_cart(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'shopping_cart/cart.html', {'cart': cart})


@login_required()
def add_to_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('shopping_cart:show_cart')
