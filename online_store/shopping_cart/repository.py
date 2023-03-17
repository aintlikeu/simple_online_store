from django.shortcuts import get_object_or_404
from django.db.models import Case, PositiveIntegerField, When, F
from shopping_cart.models import Cart, CartItem, Order, OrderItem
from catalog.models import Product


class ShoppingCartRepository:
    def __init__(self, user):
        self.user = user

    def get_cart(self):
        cart, _ = Cart.objects.get_or_create(self.user)
        return cart

    def get_all_cart_items(self):
        cart = self.get_cart()
        cart_items = CartItem.objects.filter(cart=cart)
        return cart_items

    def get_cart_item(self, product_id):
        cart = self.get_cart()
        product = get_object_or_404(Product, pk=product_id)
        cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
        return cart_item

    def add_to_cart(self, product_id):
        cart_item = self.get_cart_item(product_id)
        cart_item.quantity += 1
        cart_item.save()

    def extract_from_cart(self, product_id):
        cart_item = self.get_cart_item(product_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    def clear_cart(self):
        cart = self.get_cart()
        CartItem.objects.filter(cart=cart).delete()

    def create_order(self, form):
        order = Order.objects.create(
            user=self.user,
            address=form.cleaned_data['address'],
            phone=form.cleaned_data['phone'],
            status='PENDING'
        )
        cart_items = self.get_all_cart_items()

        # bulk creation of OrderItem for items in Shopping cart
        order_item_list = [OrderItem(order=order, product=item.product, quantity=item.quantity) for item
                           in cart_items]
        OrderItem.objects.bulk_create(order_item_list)

        # updating stocks
        Product.objects.filter(pk__in=[item.product.pk for item in cart_items]).update(
            stock=F('stock') - Case(*[When(pk=item.product.pk, then=item.quantity) for item in cart_items],
                                    output_field=PositiveIntegerField())
        )

        # clearing the shopping cart
        self.clear_cart()
