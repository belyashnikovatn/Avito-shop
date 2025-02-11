# Avito-shop



## Задачи
[x] Спроектировать модель данных 
[x] Создать проект, приложение, настроить среду
[x] Выбрать модель для профиля (User)
[x] Продумать ручки: 
[x] Создать модели
[x] Продумать уровень валидации
[x] Продумать уровень логики

## Проектирование
- Модель данных ERD
- Ручки

| url       | method       | что делает      | кто может      |
|:----------|:----------|:---------:|----------:|
| /api/info   | ---   | Получить информацию о монетах, инвентаре и истории транзакций.   | Не указано. Пусть будет только автору данных.   |
| Данные 1  | Данные 2  | Данные 3  |Данные 3  |



## Уровень моделей
## Уровень сериализаторов
## Уровень представлений

## Запуск проекта в режиме разработки 
Склонируйте проект
```bash
git clone git@github.com:belyashnikovatn/Avito-shop.git
```
В терминале выполните команды:
```bash
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cd avito_shop/
python manage.py migrate
python manage.py initadmin
python manage.py runserver
```

## Запуск проекта 
убедитесь, что у вас установлен и запущен Docker
В корне проекта выполните команду:
```bash
docker compose up --build  -d
```