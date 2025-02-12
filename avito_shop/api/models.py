from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    """Профиль сотрудника: имя + монеты."""

    username = models.CharField(
        verbose_name='Никнейм',
        unique=True,
        max_length=255,
    )
    coins = models.IntegerField(
        default=1000,
        verbose_name='Монеты'
    )

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.username


class Merch(models.Model):
    """Мерч на складе."""

    name = models.SlugField(
        verbose_name='Название',
        unique=True,
        max_length=200,
    )
    price = models.IntegerField(
        verbose_name='Цена',
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name} за {self.price}'


class Gift(models.Model):
    """Подарок монет сотруднику."""

    from_user = models.ForeignKey(
        Profile,
        related_name='sender',
        on_delete=models.CASCADE,
        verbose_name='Даритель',
    )
    to_user = models.ForeignKey(
        Profile,
        related_name='receiver',
        on_delete=models.CASCADE,
        verbose_name='Получатель',
    )
    amount = models.IntegerField(
        verbose_name='Количество',
    )
    created = models.DateTimeField(
        'Дата операции', auto_now_add=True)

    class Meta:
        verbose_name = 'подарок'
        verbose_name_plural = 'Подарки'

    def __str__(self):
        return f'{self.from_user} подарил(а) {self.to_user} {self.amount}'


class Buy(models.Model):
    """Покупка мерча."""

    user = models.ForeignKey(
        Profile,
        related_name='buyer',
        on_delete=models.CASCADE,
        verbose_name='Покупатель'
    )
    merch = models.ForeignKey(
        Merch,
        related_name='shopping',
        on_delete=models.CASCADE,
        verbose_name='Мерч')
    created = models.DateTimeField(
        'Дата операции', auto_now_add=True)

    class Meta:
        verbose_name = 'покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return f'{self.user} купил(а) {self.merch}'
