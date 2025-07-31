#!/bin/bash

# Startup script for Azure App Service
echo "Starting Sundar Marbles Django Backend..."

# Set Django settings module for production
export DJANGO_SETTINGS_MODULE=sundar_marbles.settings_production

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the production setup command
echo "Running production setup..."
python manage.py setup_production

# Start the application
echo "Starting Django application..."
gunicorn sundar_marbles.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
