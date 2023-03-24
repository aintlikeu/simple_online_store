import pytest
from django.urls import reverse
from authuser.models import User
from catalog.models import Product, Category
from shopping_cart.models import Cart, CartItem, Order, OrderItem
from shopping_cart.forms import OrderForm


@pytest.fixture
def user():
    user = User.objects.create_user(email='user@example.com', password='password')
    return user


@pytest.fixture
def product():
    product = Product.objects.create(name='Test Product',
                                     category=Category.objects.create(name='Test Category'),
                                     article_number='12356',
                                     price=9.99,
                                     stock=10,
                                     image_url='http://example.com')
    return product


@pytest.fixture
def cart(client, user):
    client.force_login(user)
    cart = Cart.objects.create(user=user)
    return cart


@pytest.fixture
def cart_item(cart, product):
    cart_item = CartItem.objects.create(
        cart=cart,
        product=product,
        quantity=5
    )
    return cart_item


@pytest.mark.django_db
def test_show_cart_view_logged_in(client, user):
    client.force_login(user)
    url = reverse('shopping_cart:show_cart')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['cart'].user == user


@pytest.mark.django_db
def test_show_cart_view_not_logged_in(client):
    url = reverse('shopping_cart:show_cart')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/auth/login?next=/cart/'


@pytest.mark.django_db
def test_add_to_cart_view(client, user, product):
    client.force_login(user)
    url = reverse('shopping_cart:add_to_cart', args=[product.pk])
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/'
    assert CartItem.objects.count() == 1
    assert CartItem.objects.get(pk=product.pk).quantity == 1


@pytest.mark.django_db
def test_extract_from_cart_view(client, product, cart_item):
    before_qty = CartItem.objects.get(pk=product.pk).quantity
    url = reverse('shopping_cart:remove_from_cart', args=[product.pk])
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('shopping_cart:show_cart')
    assert CartItem.objects.get(pk=product.pk).quantity == before_qty - 1


@pytest.mark.django_db
def test_clear_cart_view(client, cart, cart_item):
    assert CartItem.objects.filter(cart=cart).count() > 0
    url = reverse('shopping_cart:clear_cart')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('shopping_cart:show_cart')
    assert CartItem.objects.filter(cart=cart).count() == 0


def test_thank_you_view(client):
    url = reverse('shopping_cart:thank_you')
    response = client.get(url)
    assert response.status_code == 200
    assert response.templates[0].name == 'shopping_cart/thank_you.html'


@pytest.mark.django_db
def test_checkout_view_get_empty_basket(client, cart):
    url = reverse('shopping_cart:checkout')
    response = client.get(url)
    assert response.status_code == 200
    assert response.templates[0].name == 'shopping_cart/checkout.html'
    assert b'Your shopping cart is empty' in response.content


@pytest.mark.django_db
def test_checkout_view_get_not_empty_basket(client, cart, cart_item):
    url = reverse('shopping_cart:checkout')
    response = client.get(url)
    assert response.status_code == 200
    assert response.templates[0].name == 'shopping_cart/checkout.html'
    assert isinstance(response.context['form'], OrderForm)
    assert isinstance(response.context['cart'], Cart)
    assert response.context['cart'] == cart


@pytest.mark.django_db
def test_checkout_view_valid_form(client, cart, cart_item):

    valid_form = {'phone': '+79123456789',
                  'address': 'home'}

    url = reverse('shopping_cart:checkout')
    response = client.post(url, data=valid_form)
    assert response.url == reverse('shopping_cart:thank_you')
    # assert Order.objects.count() == 1


@pytest.mark.django_db
def test_checkout_view_invalid_form():
    pass
