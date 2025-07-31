#!/bin/bash

# Startup script for Azure App Service
echo "Starting Sundar Marbles Django Backend..."

# FORCE Django settings module for production  
export DJANGO_SETTINGS_MODULE=sundar_marbles.settings_production

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Start the application
echo "Starting Django application..."
gunicorn sundar_marbles.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
