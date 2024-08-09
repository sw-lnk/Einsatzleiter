#!/bin/ash

echo "Apply database migrations"

python manage.py migrate
python manage.py migrate --run-syncdb

exec "$@"
