from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Case, PositiveIntegerField, When, F
from shopping_cart.models import Cart, CartItem, Order, OrderItem
from catalog.models import Product
from shopping_cart.forms import OrderForm


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
    if_enough_stocks(request)
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
    CartItem.objects.filter(cart=cart).delete()
    return redirect('shopping_cart:show_cart')


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request):
        if_enough_stocks(request)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        form = OrderForm()
        return render(request, 'shopping_cart/checkout.html', {'cart': cart, 'form': form})

    def post(self, request):
        form = OrderForm(request.POST)
        # placing the order
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone'],
                status='PENDING'
            )
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.filter(cart=cart)

            # bulk creation of OrderItem for items in Shopping cart
            order_item_list = [OrderItem(order=order, product=item.product, quantity=item.quantity) for item
                               in cart_item]
            OrderItem.objects.bulk_create(order_item_list)

            # updating stocks
            Product.objects.filter(pk__in=[item.product.pk for item in cart_item]).update(
                stock=F('stock') - Case(*[When(pk=item.product.pk, then=item.quantity) for item in cart_item],
                                        output_field=PositiveIntegerField())
            )

            # clearing the shopping cart
            cart_item.delete()
            return redirect('shopping_cart:thank_you')
        else:
            messages.error(request, 'Something went wrong. Please try again', extra_tags='alert-danger')
            return redirect('shopping_cart:checkout')


def thank_you(request):
    return render(request, 'shopping_cart/thank_you.html')


def if_enough_stocks(request):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart)
    # if there are not enough stocks, changes quantity in the shopping cart
    for item in cart_item:
        if item.quantity > item.product.stock:
            item.quantity = item.product.stock
            item.save()
            messages.error(request, f'{item.product.name} - {item.product.stock} in stock', extra_tags='alert-danger')
