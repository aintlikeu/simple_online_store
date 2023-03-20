from django.contrib import messages


def if_enough_stocks(request, cart_items):
    """
    if there are not enough stocks, changes quantity in the shopping cart and shows a message
    """
    for item in cart_items:
        if item.quantity > item.product.stock:
            item.quantity = item.product.stock
            item.save()
            messages.error(request, f'{item.product.name} - {item.product.stock} in stock', extra_tags='alert-danger')
