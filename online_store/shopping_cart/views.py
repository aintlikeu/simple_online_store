from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from catalog.models import Product
from .forms import OrderForm

def show_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shopping_cart/cart.html', {'cart': cart})


@login_required()
def add_to_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    # redirect to the same page from where you added item to the shopping cart
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def remove_from_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('shopping_cart:show_cart')


@login_required()
def clear_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart = CartItem.objects.filter(cart=cart).delete()
    return redirect('shopping_cart:show_cart')


@login_required()
def checkout(request):
    if request.method == 'GET':
        cart, _ = Cart.objects.get_or_create(user=request.user)
        form = OrderForm()
        return render(request, 'shopping_cart/checkout.html', {'cart': cart, 'form': form})