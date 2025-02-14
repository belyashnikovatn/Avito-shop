import pytest
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Profile


@pytest.fixture
def api_client():
    """Фикстура для клиента API"""
    return APIClient()


@pytest.fixture
def create_user(db):
    """Фикстура для создания тестового пользователя"""
    return Profile.objects.create_user(
        username='testuser',
        password='testpassword')


@pytest.mark.django_db
def test_successful_auth_existing_user(api_client, create_user):
    """Успешная аутентификация существующего пользователя"""
    url = '/api/auth/'
    response = api_client.post(
        url,
        {'username': 'testuser', 'password': 'testpassword'},
        format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'JWT-токен для доступа к защищенным ресурсам.' in response.json()


@pytest.mark.django_db
def test_successful_auth_new_user(api_client):
    """Регистрация нового пользователя"""
    url = '/api/auth/'
    response = api_client.post(
        url,
        {'username': 'newuser', 'password': 'newpassword'},
        format='json')

    assert response.status_code == status.HTTP_200_OK
    assert Profile.objects.filter(username='newuser').exists()


@pytest.mark.django_db
def test_auth_empty_data(api_client):
    """С пустыми данными невозможно"""
    url = '/api/auth/'
    response = api_client.post(url, {}, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_new_user_starts_with_1000_coins(api_client):
    """Новый пользователь создаётся с 1000 монетами"""
    url = '/api/auth/'
    response = api_client.post(
        url,
        {'username': 'newuser', 'password': 'newpassword'},
        format='json')

    assert response.status_code == status.HTTP_200_OK

    user = Profile.objects.get(username='newuser')
    assert user.coins == 1000
