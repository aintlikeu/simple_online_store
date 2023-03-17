from django.contrib import messages
from django.shortcuts import get_object_or_404
from shopping_cart.repository import ShoppingCartRepository
from catalog.models import Product


def if_enough_stocks(request):
    """
    if there are not enough stocks, changes quantity in the shopping cart and shows a message
    :param request:
    :return: None
    """
    cart_repo = ShoppingCartRepository(request.user)
    cart_items = cart_repo.get_all_cart_items()
    for item in cart_items:
        if item.quantity > item.product.stock:
            item.quantity = item.product.stock
            item.save()
            messages.error(request, f'{item.product.name} - {item.product.stock} in stock', extra_tags='alert-danger')


def get_product_by_id(product_id):
    return get_object_or_404(Product, pk=product_id)