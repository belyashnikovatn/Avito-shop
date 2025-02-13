#!/usr/bin/env sh
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py initadmin
python manage.py loaddata merch.json
python manage.py collectstatic --no-input && cp -r /app/collected_static/. /backend_static/static/

gunicorn avito_shop.wsgi:application --bind 0.0.0.0:8080 --workers=1