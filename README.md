# Avito-shop



## Задачи

## Проектирование

## Уровень моделей
## Уровень представлений
## Уровень сериализаторов

## Запуск проекта в режиме разработки 
Склонируйте проект
```bash
git clone https://github.com/belyashnikovatn/
```
В терминале выполните команды:
```bash
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cd avito_shop/
python manage.py migrate
LOADDATA
python manage.py runserver
```

## Запуск проекта 
убедитесь, что у вас установлен и запущен Docker
В корне проекта выполните команду:
```bash
docker compose up --build  -d
```