import pytest
from django.urls import reverse
from catalog.models import Product, Category


@pytest.mark.django_db
def test_product_list_view(client):
    url = reverse('catalog:product_list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'object_list' in response.context


@pytest.mark.django_db
def test_product_detail_view(client):
    product = Product.objects.create(name='Test Product',
                                     category=Category.objects.create(name='Test Category'),
                                     article_number='12356',
                                     price=9.99,
                                     stock=10,
                                     image_url='http://example.com')
    url = reverse('catalog:product_detail', args=[product.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert 'object' in response.context
    assert response.context['object'] == product
