# Avito-shop

## Функционал:
- авторизация
- просмотр профиля
- подарить монеты
- купить мерч
- просмотреть список мерча

- при запуске в контейнерах автоматиечски создаётся админ и загружаются данные в мерч 
- логирование 

## Задачи
[x] Спроектировать модель данных 
[x] Создать проект, приложение, настроить среду
[x] Выбрать модель для профиля (User)
[x] Продумать ручки
[x] Создать модели
[x] Продумать уровень валидации
[x] Продумать уровень логики

## Проектирование
- Модель данных ERD
- Ручки (дополнительно: вывод мерча для всех, список всех юзеров для админа)

| url       | method       | что делает      | кто может      |
|:----------|:----------|:---------:|----------:|
| /api/info   | get   | Получить информацию о монетах, инвентаре и истории транзакций.   | Юзер видит только свои данные   |
| /api/sendCoin | post  | Отправить монеты другому пользователю.  | Авторизованный юзер  |
| /api/buy/{item}  | get (Странно, что get, вроде не по REST) | Купить предмет за монеты.  |Авторизованный юзер  |
| /api/auth  | post | Аутентификация и получение JWT-токена. При первой аутентификации пользователь создается автоматически.  |Любой юзер |



## Уровень моделей
- Profile: username, coins(default=1000)
- Merch: name, price

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