import pytest
from rest_framework.test import APIClient

from api.models import Merch, Buy, Profile


@pytest.mark.django_db
def test_buy_merch():
    """E2E тест для покупки мерча."""

    client = APIClient()

    # Создаем пользователя
    user = Profile.objects.create_user(
        username='C3PO', password='C3PO_BEST')

    # Логинимся и получаем JWT-токен
    response = client.post(
        '/api/auth/', {'username': 'C3PO', 'password': 'C3PO_BEST'})
    assert response.status_code == 200
    token = response.data['JWT-токен для доступа к защищенным ресурсам.']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Создаем мерч
    merch = Merch.objects.create(name='tshirt', price=500)

    # Проверяем баланс перед покупкой
    user.refresh_from_db()
    assert user.coins == 1000

    # Покупаем мерч
    response = client.post(f'/api/buy/{merch.name}/')
    assert response.status_code == 200

    # Проверяем, что монеты списались
    user.refresh_from_db()
    assert user.coins == 500

    # Проверяем, что покупка записалась в БД
    assert Buy.objects.filter(user=user, merch=merch).exists()
