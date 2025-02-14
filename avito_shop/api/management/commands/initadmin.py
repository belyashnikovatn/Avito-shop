import logging
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

load_dotenv()
User = get_user_model()

logging.basicConfig(
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


class Command(BaseCommand):
    help = 'Создаёт админа по данным из env файла.'

    def handle(self, *args, **options):

        username = os.getenv('username', 'admin_avito')
        email = os.getenv('email', 'admin_example@gmail.com')
        password = os.getenv('password', 'avito_12345678')

        if not User.objects.filter(username=username).exists():
            logging.info('Создаю аккаунт для %s (%s)' % (username, email))
            try:
                User.objects.create_superuser(
                    email=email, username=username,
                    password=password,
                )
                logging.info('Админ успешно создан.')
            except Exception as error:
                logging.error(f'Ошибка {error}!')
        else:
            logging.info('Админ уже создан.')
