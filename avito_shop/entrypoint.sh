#!/bin/sh
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py initadmin
python manage.py loaddata merch.json
python manage.py collectstatic --no-input --clear && cp -r /app/collected_static/. /backend_static/static/
gunicorn -b 0.0.0.0:8080 avito_shop.wsgi
