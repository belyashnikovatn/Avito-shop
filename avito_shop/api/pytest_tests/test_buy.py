import pytest
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Merch, Buy, Profile


@pytest.fixture
def api_client():
    """Фикстура для API-клиента."""
    return APIClient()


@pytest.fixture
def user():
    """Создаем тестового пользователя."""
    return Profile.objects.create_user(
        username='testuser', password='password123', coins=1000)


@pytest.fixture
def merch():
    """Создаем тестовый мерч."""
    return Merch.objects.create(name='test-merch', price=500)


@pytest.mark.django_db
def test_successful_purchase(api_client, user, merch):
    """Тест успешной покупки мерча."""
    api_client.force_authenticate(user=user)

    response = api_client.get(f'/api/buy/{merch.name}/')

    user.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert user.coins == 500
    assert Buy.objects.filter(user=user, merch=merch).exists()


@pytest.mark.django_db
def test_purchase_not_enough_coins(api_client, user, merch):
    """Тест, если у пользователя недостаточно монет."""
    user.coins = 400
    user.save()

    api_client.force_authenticate(user=user)
    response = api_client.get(f'/api/buy/{merch.name}/')

    user.refresh_from_db()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert user.coins == 400
    assert not Buy.objects.filter(user=user, merch=merch).exists()


@pytest.mark.django_db
def test_purchase_nonexistent_merch(api_client, user):
    """Тест покупки несуществующего мерча."""
    api_client.force_authenticate(user=user)

    response = api_client.get('/api/buy/nonexistent-merch/')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_unauthorized_purchase(api_client, merch):
    """Тест неавторизованного запроса."""
    response = api_client.get(f'/api/buy/{merch.name}/')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
