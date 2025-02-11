from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    username = models.CharField(
        verbose_name='Никнейм',
        unique=True,
        max_length=255,
    )
    coins = models.IntegerField(default=1000, verbose_name='Монеты')

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.username
