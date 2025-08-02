#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sundar_marbles.settings')
django.setup()

from products.models import Product

print("=== CURRENT PRODUCTS IN DATABASE ===")
for product in Product.objects.all():
    print(f"ID: {product.id}")
    print(f"Name: {product.name}")
    print(f"Image: {product.image}")
    print(f"Image URL: {product.image.url if product.image else 'No image'}")
    print("-" * 50)

print(f"\nTotal products: {Product.objects.count()}")
