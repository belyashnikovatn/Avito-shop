from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    coins = models.IntegerField(default=1000, verbose_name='Монеты')

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.username
