from django.db import models
from catalog.models import Product
from authuser.models import User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} * {self.quantity}'

    def get_cost(self):
        return self.product.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    placed_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    phone = models.CharField(max_length=10)
    status = models.CharField(max_length=100)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_cost(self):
        return self.product.price * self.quantity
