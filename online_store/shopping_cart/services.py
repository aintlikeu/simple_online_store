from django.db.models.query import QuerySet
from shopping_cart.models import CartItem


class NotEnoughStockException(Exception):
    pass


def if_enough_stocks(cart_items: QuerySet[CartItem]) -> None:
    """
    if there are not enough stocks, changes quantity in the shopping cart and raises an exception
    """
    for item in cart_items:
        if item.quantity > item.product.stock:
            item.quantity = item.product.stock
            item.save()
            error_msg = f'{item.product.name} - {item.product.stock} in stock'
            raise NotEnoughStockException(error_msg)
