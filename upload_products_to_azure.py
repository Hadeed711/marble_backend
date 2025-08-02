#!/usr/bin/env python
"""
Script to upload existing product images to Azure Blob Storage
and populate the Django database with products
"""

import os
import sys
import django
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from decouple import config

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sundar_marbles.settings')
django.setup()

# Now import Django models
from products.models import Product, Category

def upload_products_to_azure():
    """Upload local product images to Azure Blob Storage and create database entries"""
    
    # Azure storage configuration
    AZURE_ACCOUNT_NAME = config('AZURE_ACCOUNT_NAME')
    AZURE_ACCOUNT_KEY = config('AZURE_ACCOUNT_KEY')
    AZURE_CONTAINER = config('AZURE_CONTAINER', default='media')
    
    # Create blob service client
    blob_service_client = BlobServiceClient(
        account_url=f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net",
        credential=AZURE_ACCOUNT_KEY
    )
    
    # Get or create categories
    marble_cat, _ = Category.objects.get_or_create(
        slug='marble', 
        defaults={'name': 'Marble'}
    )
    granite_cat, _ = Category.objects.get_or_create(
        slug='granite', 
        defaults={'name': 'Granite'}
    )
    
    # Define your frontend images path (adjust this path to your frontend)
    frontend_assets = Path("../marble-tiles-site/src/assets/products")
    
    # Product mappings from your frontend
    product_mappings = [
        {'file': 'black_gold.jpg', 'name': 'Black Gold Marble', 'price': '12000', 'category': marble_cat, 'description': 'Premium black marble with gold veining'},
        {'file': 'star_black.jpg', 'name': 'Star Black Marble', 'price': '8500', 'category': marble_cat, 'description': 'Elegant black marble with star patterns'},
        {'file': 'taweera.png', 'name': 'Taweera Granite', 'price': '9200', 'category': granite_cat, 'description': 'Durable granite with natural patterns'},
        {'file': 'jet_black.png', 'name': 'Jet Black Marble', 'price': '7800', 'category': marble_cat, 'description': 'Deep black marble for modern designs'},
        {'file': 'tropical_grey.png', 'name': 'Tropical Grey Granite', 'price': '10500', 'category': granite_cat, 'description': 'Grey granite with tropical patterns'},
        {'file': 'booti_seena.png', 'name': 'Booti Seena Granite', 'price': '8200', 'category': granite_cat, 'description': 'Classic granite with speckled finish'},
        {'file': 'sunny_white.jpg', 'name': 'Sunny White Marble', 'price': '6800', 'category': marble_cat, 'description': 'Bright white marble for luxury spaces'},
        {'file': 'sunny_grey.jpg', 'name': 'Sunny Grey Marble', 'price': '7200', 'category': marble_cat, 'description': 'Sophisticated grey marble with subtle veining'},
    ]
    
    print(f"Starting product upload to Azure Blob Storage...")
    print(f"Container: {AZURE_CONTAINER}")
    print(f"Account: {AZURE_ACCOUNT_NAME}")
    print(f"Processing {len(product_mappings)} products...")
    
    uploaded_count = 0
    
    for i, mapping in enumerate(product_mappings, 1):
        print(f"\n📦 Processing product {i}/{len(product_mappings)}: {mapping['name']}")
        try:
            # Check if product already exists in database
            existing_product = Product.objects.filter(name=mapping['name']).first()
            
            if existing_product:
                print(f"🔍 Debug - {mapping['name']} current image: {str(existing_product.image) if existing_product.image else 'None'}")
            
            # Force upload to Azure Blob Storage (comment out the skip condition for now)
            # if existing_product and existing_product.image and str(existing_product.image).startswith('products/'):
            #     print(f"⏭️  Skipping {mapping['name']} - already uploaded to Azure Blob Storage")
            #     continue
            
            # Full path to local image
            local_image_path = frontend_assets / mapping['file']
            
            if not local_image_path.exists():
                print(f"❌ Local image not found: {local_image_path}")
                continue
            
            # Upload to Azure Blob Storage
            blob_name = f"products/{local_image_path.name}"
            blob_client = blob_service_client.get_blob_client(
                container=AZURE_CONTAINER, 
                blob=blob_name
            )
            
            print(f"📤 Uploading {local_image_path.name}...")
            
            with open(local_image_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            
            # Create or update database entry
            if existing_product:
                # Update existing product with image
                existing_product.image = blob_name
                existing_product.price = mapping['price']
                existing_product.description = mapping['description']
                existing_product.save()
                print(f"✅ Updated existing product with image: {mapping['name']}")
            else:
                # Create new product
                product = Product.objects.create(
                    name=mapping['name'],
                    image=blob_name,  # This will be the path in Azure
                    category=mapping['category'],
                    price=mapping['price'],
                    description=mapping['description'],
                    is_featured=True if mapping['name'] in ['Black Gold Marble', 'Sunny White Marble'] else False
                )
                print(f"✅ Successfully uploaded and created: {mapping['name']}")
            
            uploaded_count += 1
            
        except Exception as e:
            print(f"❌ Error processing {mapping['name']}: {str(e)}")
    
    print(f"\n🎉 Product upload complete! Uploaded {uploaded_count} products to Azure Blob Storage and database.")
    print(f"📊 Total database products: {Product.objects.count()}")

if __name__ == "__main__":
    upload_products_to_azure()
