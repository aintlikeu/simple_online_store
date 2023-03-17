from django.contrib import messages
from shopping_cart.repository import ShoppingCartRepository


def if_enough_stocks(request):
    """
    if there are not enough stocks, changes quantity in the shopping cart and shows a message
    :param request:
    :return: None
    """
    repository = ShoppingCartRepository(request.user)
    cart_items = repository.get_all_cart_items()
    for item in cart_items:
        if item.quantity > item.product.stock:
            item.quantity = item.product.stock
            item.save()
            messages.error(request, f'{item.product.name} - {item.product.stock} in stock', extra_tags='alert-danger')
