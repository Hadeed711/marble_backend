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

print("=== PRODUCTS WITHOUT IMAGES ===")
products_without_images = Product.objects.filter(image='')
for product in products_without_images:
    print(f"- {product.name}")

print(f"\nMissing images: {products_without_images.count()}")
print(f"Products with images: {Product.objects.exclude(image='').count()}")
print(f"Total products: {Product.objects.count()}")
