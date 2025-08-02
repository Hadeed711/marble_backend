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

print("=== PRODUCT IMAGE STATUS ===")
for product in Product.objects.all()[:5]:  # Just first 5
    has_image = bool(product.image)
    print(f"{product.name}: {'✅ HAS IMAGE' if has_image else '❌ NO IMAGE'}")
    if has_image:
        print(f"  Image path: {product.image}")
    print()

print(f"Products with images: {Product.objects.exclude(image='').count()}")
print(f"Products without images: {Product.objects.filter(image='').count()}")
print(f"Total products: {Product.objects.count()}")
