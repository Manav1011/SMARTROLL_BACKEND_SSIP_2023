#!/bin/bash
python manage.py makemigrations;

python manage.py migrate;

python manage.py flush --noinput

python manage.py loaddata datadump.json

python manage.py collectstatic --noinput