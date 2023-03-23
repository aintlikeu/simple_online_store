import pytest
from django.urls import reverse
from authuser.forms import LoginUserForm, RegistrationForm
from authuser.models import User


@pytest.fixture
def user():
    user = User.objects.create_user(email='user@example.com', password='password')
    return user


@pytest.fixture
def authenticated_user(client):
    user = User.objects.create_user(email='user@example.com', password='password')
    client.login(username='user@example.com', password='password')
    return user


def test_register_view_get(client):
    url = reverse('authuser:register')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], RegistrationForm)


@pytest.mark.django_db
def test_register_view_valid_form(client):
    valid_form = {
        'email': 'user@example.com',
        'password1': 'password',
        'password2': 'password'
    }
    url = reverse('authuser:register')
    response = client.post(url, data=valid_form)
    assert response.status_code == 302
    assert response.url == reverse('catalog:product_list')
    assert User.objects.count() == 1
    assert User.objects.filter(email=valid_form['email']).exists()


@pytest.mark.django_db
def test_register_view_invalid_form(client):
    invalid_form = {
        'email': 'user',
        'password1': 'passw',
        'password2': 'password'
    }
    url = reverse('authuser:register')
    response = client.post(url, data=invalid_form)
    assert response.status_code == 302
    assert response.url == reverse('authuser:register')
    assert User.objects.count() == 0


def test_login_view_get(client):
    url = reverse('authuser:login')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], LoginUserForm)


@pytest.mark.django_db
def test_login_view_valid_form(client, user):
    valid_form = {'username': 'user@example.com', 'password': 'password'}
    url = reverse('authuser:login')
    response = client.post(url, data=valid_form)
    assert response.status_code == 302
    assert response.url == reverse('catalog:product_list')


@pytest.mark.django_db
def test_login_view_invalid_form(client, user):
    invalid_form = {'username': 'user2@example.com', 'password': 'password'}
    url = reverse('authuser:login')
    response = client.post(url, data=invalid_form)
    assert response.status_code == 302
    assert response.url == reverse('authuser:login')


@pytest.mark.django_db
def test_logout_view(client, authenticated_user):
    url = reverse('authuser:logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('catalog:product_list')
