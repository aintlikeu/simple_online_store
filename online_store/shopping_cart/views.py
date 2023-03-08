from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart
from catalog.models import Product

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'shopping_cart/cart.html', {'cart_items': cart_items})

@login_required()
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('shopping_cart:cart')


