import pytest
from rest_framework.test import APIClient

from api.models import Gift, Profile


@pytest.mark.django_db
def test_send_coins():
    """E2E тест для передачи монеток."""

    client1 = APIClient()
    client2 = APIClient()

    # Создаем пользователей
    user1 = Profile.objects.create_user(username='Luke', password='LukeLuke')
    user2 = Profile.objects.create_user(username='Han', password='hahahan')
    user3 = Profile.objects.create_user(username='Leia', password='strongpsw')

    # Аутентификация Люка
    response = client1.post(
        '/api/auth/', {'username': 'Luke', 'password': 'LukeLuke'})
    assert response.status_code == 200
    token = response.data['JWT-токен для доступа к защищенным ресурсам.']
    client1.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Аутентификация Хана
    response = client2.post(
        '/api/auth/', {'username': 'Han', 'password': 'hahahan'})
    assert response.status_code == 200
    token = response.data['JWT-токен для доступа к защищенным ресурсам.']
    client2.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Проверяем начальный баланс
    user1.refresh_from_db()
    user2.refresh_from_db()
    user3.refresh_from_db()
    assert user1.coins == 1000
    assert user2.coins == 1000
    assert user3.coins == 1000

    # Отправляем 200 монет от Люка к Хану
    response = client1.post(
        '/api/sendCoin/', {'toUser': 'Han', 'amount': 200}, format='json')
    assert response.status_code == 200

    # Отправляем 200 монет от Хана к Лее
    response = client2.post(
        '/api/sendCoin/', {'toUser': 'Leia', 'amount': 500}, format='json')
    assert response.status_code == 200

    # Проверяем обновленный баланс
    user1.refresh_from_db()
    user2.refresh_from_db()
    user3.refresh_from_db()
    assert user1.coins == 800
    assert user2.coins == 700
    assert user3.coins == 1500

    # Проверяем, что записи о переводе есть в модели Gift
    assert Gift.objects.filter(
        from_user=user1, to_user=user2, amount=200).exists()
    assert Gift.objects.filter(
        from_user=user2, to_user=user3, amount=500).exists()
    assert Gift.objects.count() == 2
