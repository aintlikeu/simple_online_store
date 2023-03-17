from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from shopping_cart.forms import OrderForm
from shopping_cart.repository import ShoppingCartRepository
from shopping_cart.services import if_enough_stocks


def show_cart_view(request):
    repository = ShoppingCartRepository(request.user)
    cart = repository.get_cart()
    return render(request, 'shopping_cart/cart.html', {'cart': cart})


@login_required()
def add_to_cart_view(request, product_id):
    repository = ShoppingCartRepository(request.user)
    repository.add_to_cart(product_id)
    if_enough_stocks(request)
    # redirect to the same page from where you added item to the shopping cart
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def extract_from_cart_view(request, product_id):
    repository = ShoppingCartRepository(request.user)
    repository.extract_from_cart(product_id)
    return redirect('shopping_cart:show_cart')


@login_required()
def clear_cart_view(request):
    repository = ShoppingCartRepository(request.user)
    repository.clear_cart()
    return redirect('shopping_cart:show_cart')


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request):
        repository = ShoppingCartRepository(request.user)
        if_enough_stocks(request)
        cart = repository.get_cart()
        form = OrderForm()
        return render(request, 'shopping_cart/checkout.html', {'cart': cart, 'form': form})

    def post(self, request):
        repository = ShoppingCartRepository(request.user)
        form = OrderForm(request.POST)
        # placing the order
        if form.is_valid():
            repository.create_order(form)
            return redirect('shopping_cart:thank_you')
        else:
            messages.error(request, 'Something went wrong. Please try again', extra_tags='alert-danger')
            return redirect('shopping_cart:checkout')


def thank_you_view(request):
    return render(request, 'shopping_cart/thank_you.html')
