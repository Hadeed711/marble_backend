#!/bin/bash

# Azure App Service Startup Script for Django
echo "=== Starting Sundar Marbles Django Backend ==="

# Force production environment
export DJANGO_SETTINGS_MODULE=sundar_marbles.settings_production
export DEBUG=False
export SECRET_KEY="kTvi#=!ucz6tMDQpqK=W#t0y^y7yzXxLUCN5xc^uy3F^MzAv(N"
export DATABASE_URL="postgresql://neondb_owner:npg_qrXsNK3Jpk8i@ep-divine-tooth-a8gxgnc6-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"

# CRITICAL: Run migrations to fix the price field issue
echo "🔄 Running database migrations..."
python manage.py migrate products --noinput
echo "✅ Migrations completed"

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Test database connection
echo "Testing database connection..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sundar_marbles.settings_production')
import django
django.setup()
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
        print('✅ Database connection successful')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
"

# Run database migrations with verbose output
echo "Running database migrations..."
python manage.py migrate --verbosity=2

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell << 'PYTHON_SCRIPT'
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sundar_marbles.settings_production')
import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Delete existing admin user if exists
if User.objects.filter(username='admin').exists():
    User.objects.filter(username='admin').delete()
    print("Deleted existing admin user")

# Create new superuser
try:
    user = User.objects.create_superuser('admin', 'admin@sundarmarbles.com', 'admin123456')
    print("✅ Superuser created successfully: admin / admin123456")
except Exception as e:
    print(f"❌ Failed to create superuser: {e}")

# Verify user creation
if User.objects.filter(username='admin').exists():
    print("✅ Admin user verified in database")
else:
    print("❌ Admin user not found in database")
PYTHON_SCRIPT

# Start the application with gunicorn
echo "Starting Django application with gunicorn..."
exec gunicorn azure_wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 300 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --log-level info
