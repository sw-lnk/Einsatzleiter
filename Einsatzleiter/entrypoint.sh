#!/bin/ash

echo "Apply database migrations"

python manage.py makemigrations users
python manage.py migrate
python manage.py migrate --run-syncdb

python manage.py runscript botuser
python manage.py createsuperuser --noinput

exec "$@"
