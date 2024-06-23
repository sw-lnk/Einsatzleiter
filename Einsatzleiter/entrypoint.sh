#!/bin/ash

echo "Apply database migrations"

rm -r users/migrations/
python manage.py makemigrations users
python manage.py migrate
python manage.py migrate --run-syncdb

python manage.py runscript botuser

exec "$@"