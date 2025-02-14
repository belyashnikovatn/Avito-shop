import pytest
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Profile, Gift


@pytest.fixture
def api_client():
    """Фикстура для API-клиента."""
    return APIClient()


@pytest.fixture
def user1():
    """Создаем первого тестового пользователя."""
    return Profile.objects.create_user(
        username='user1', password='password123')


@pytest.fixture
def user2():
    """Создаем второго тестового пользователя."""
    return Profile.objects.create_user(
        username='user2', password='password123')


@pytest.mark.django_db
def test_successful_coin_transfer(api_client, user1, user2):
    """Тест успешного перевода монет."""
    api_client.force_authenticate(user=user1)

    data = {
        'toUser': 'user2',
        'amount': 200
    }

    response = api_client.post('/api/sendCoin/', data, format='json')

    user1.refresh_from_db()
    user2.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert response.data['description'] == 'Успешный ответ.'
    assert user1.coins == 800
    assert user2.coins == 1200
    assert Gift.objects.filter(
        from_user=user1, to_user=user2, amount=200).exists()


@pytest.mark.django_db
def test_transfer_to_self(api_client, user1):
    """Тест попытки отправки монет самому себе."""
    api_client.force_authenticate(user=user1)

    data = {
        'toUser': 'user1',
        'amount': 200
    }

    response = api_client.post('/api/sendCoin/', data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_transfer_more_than_balance(api_client, user1, user2):
    """Тест попытки отправки больше, чем есть на балансе."""
    api_client.force_authenticate(user=user1)

    data = {
        'toUser': 'user2',
        'amount': 1200
    }

    response = api_client.post('/api/sendCoin/', data, format='json')

    user1.refresh_from_db()
    user2.refresh_from_db()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert user1.coins == 1000
    assert user2.coins == 1000
    assert not Gift.objects.filter(from_user=user1, to_user=user2).exists()


@pytest.mark.django_db
def test_transfer_to_non_existent_user(api_client, user1):
    """Тест попытки перевода несуществующему пользователю."""
    api_client.force_authenticate(user=user1)

    data = {
        'toUser': 'non_existent_user',
        'amount': 100
    }

    response = api_client.post('/api/sendCoin/', data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_transfer_zero_or_negative_amount(api_client, user1, user2):
    """Тест попытки перевести 0 или отрицательное количество монет."""
    api_client.force_authenticate(user=user1)

    data_zero = {
        'toUser': 'user2',
        'amount': 0
    }
    response_zero = api_client.post('/api/sendCoin/', data_zero, format='json')

    data_negative = {
        'toUser': 'user2',
        'amount': -100
    }
    response_negative = api_client.post(
        '/api/sendCoin/',
        data_negative, format='json')

    assert response_zero.status_code == status.HTTP_400_BAD_REQUEST

    assert response_negative.status_code == status.HTTP_400_BAD_REQUEST
