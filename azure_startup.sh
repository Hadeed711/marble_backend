#!/bin/bash

echo "=== AZURE DEPLOYMENT SCRIPT ==="
echo "Forcing production settings..."

# Force set environment variable
export DJANGO_SETTINGS_MODULE=sundar_marbles.settings_production

# Show which settings we're using
echo "Using Django settings: $DJANGO_SETTINGS_MODULE"

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations with production settings
echo "Running database migrations..."
python manage.py migrate --settings=sundar_marbles.settings_production

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=sundar_marbles.settings_production

# Create superuser if needed
echo "Creating admin user..."
python manage.py shell --settings=sundar_marbles.settings_production << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@sundarmarbles.com', 'sundar123')
    print('Superuser created: admin/sundar123')
else:
    print('Superuser already exists')
EOF

echo "=== STARTING APPLICATION ==="
# Start gunicorn with explicit settings
gunicorn sundar_marbles.wsgi:application --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=sundar_marbles.settings_production --timeout 600 --workers 1
