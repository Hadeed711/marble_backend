#!/bin/bash

# Azure Production Deployment Script
# Fixes admin panel internal server error and ensures proper blob storage integration

echo "🚀 Starting Azure Production Deployment..."

# Step 1: Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Step 2: Run database migrations
echo "🗃️  Running database migrations..."
python manage.py migrate

# Step 3: Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Step 4: Test Azure Blob Storage connectivity
echo "☁️  Testing Azure Blob Storage..."
python manage.py test_production_storage

# Step 5: Create superuser if needed (optional)
echo "👤 Creating superuser (if needed)..."
# python manage.py createsuperuser --noinput --username admin --email admin@sundarmarbles.com

echo "✅ Deployment completed!"
echo ""
echo "🔗 Test URLs:"
echo "   Admin: https://www.sundarmarbles.live/admin/"
echo "   Add Product: https://www.sundarmarbles.live/admin/products/product/add/"
echo "   Products Page: https://www.sundarmarbles.live/products"
echo "   Blob Storage: https://sundarmarbles.blob.core.windows.net/media/products/"
echo ""
echo "🎯 Expected workflow:"
echo "   1. Add product in admin panel → Saves to database"
echo "   2. Upload image → Saves to Azure Blob Storage"  
echo "   3. View products page → Images load from blob storage"
