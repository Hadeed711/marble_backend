#!/bin/bash

# Force production settings
export DJANGO_SETTINGS_MODULE=sundar_marbles.settings_production

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput

# Start gunicorn with production settings
exec gunicorn sundar_marbles.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 300
