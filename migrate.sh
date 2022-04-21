#!/bin/sh

python manage.py flush --no-input
python manage.py migrate
python load_fixtures.py

exec "$@"
