#!/usr/bin/env python
"""
Script to upload existing gallery images to Azure Blob Storage
and populate the Django database
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
from gallery.models import GalleryImage, GalleryCategory

def upload_images_to_azure():
    """Upload local images to Azure Blob Storage and create database entries"""
    
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
    stairs_cat, _ = GalleryCategory.objects.get_or_create(
        slug='stairs', 
        defaults={'name': 'Stairs'}
    )
    floors_cat, _ = GalleryCategory.objects.get_or_create(
        slug='floors', 
        defaults={'name': 'Floors'}
    )
    mosaic_cat, _ = GalleryCategory.objects.get_or_create(
        slug='mosaic', 
        defaults={'name': 'Mosaic'}
    )
    others_cat, _ = GalleryCategory.objects.get_or_create(
        slug='others', 
        defaults={'name': 'Others'}
    )
    
    # Define your frontend images path (adjust this path to your frontend)
    frontend_assets = Path("../marble-tiles-site/src/assets")
    
    # Image mappings from your frontend
    image_mappings = [
        # Stairs (18 images)
        {'file': 'stairs/gallery16.jpg', 'title': 'Premium Marble Staircase Design', 'category': stairs_cat, 'location': 'Faisalabad'},
        {'file': 'stairs/gallery33.jpg', 'title': 'Elegant Curved Staircase', 'category': stairs_cat, 'location': 'Lahore'},
        {'file': 'stairs/gallery34.jpg', 'title': 'Modern Spiral Stairs', 'category': stairs_cat, 'location': 'Karachi'},
        {'file': 'stairs/gallery35.jpg', 'title': 'Classic Marble Steps', 'category': stairs_cat, 'location': 'Islamabad'},
        {'file': 'stairs/gallery39.jpg', 'title': 'Luxury Staircase Installation', 'category': stairs_cat, 'location': 'Faisalabad'},
        {'file': 'stairs/gallery41.jpg', 'title': 'Contemporary Stair Design', 'category': stairs_cat, 'location': 'Lahore'},
        {'file': 'stairs/gallery47.jpg', 'title': 'Granite Step Construction', 'category': stairs_cat, 'location': 'Multan'},
        {'file': 'stairs/gallery48.jpg', 'title': 'Premium Stair Finishing', 'category': stairs_cat, 'location': 'Rawalpindi'},
        {'file': 'stairs/gallery49.jpg', 'title': 'Marble Staircase with Railing', 'category': stairs_cat, 'location': 'Gujranwala'},
        {'file': 'stairs/gallery5.jpg', 'title': 'Designer Staircase Project', 'category': stairs_cat, 'location': 'Sialkot'},
        {'file': 'stairs/gallery52.jpg', 'title': 'Royal Staircase Design', 'category': stairs_cat, 'location': 'Peshawar'},
        {'file': 'stairs/gallery53.jpg', 'title': 'Executive Stair Installation', 'category': stairs_cat, 'location': 'Quetta'},
        {'file': 'stairs/gallery54.jpg', 'title': 'Curved Marble Steps', 'category': stairs_cat, 'location': 'Hyderabad'},
        {'file': 'stairs/gallery55.jpg', 'title': 'Premium Staircase Work', 'category': stairs_cat, 'location': 'Sargodha'},
        {'file': 'stairs/gallery56.jpg', 'title': 'Modern Stair Architecture', 'category': stairs_cat, 'location': 'Bahawalpur'},
        {'file': 'stairs/gallery65.jpg', 'title': 'Elegant Staircase Design', 'category': stairs_cat, 'location': 'Sukkur'},
        {'file': 'stairs/gallery66.jpg', 'title': 'Luxury Marble Stairway', 'category': stairs_cat, 'location': 'Larkana'},
        {'file': 'stairs/gallery7.jpg', 'title': 'Designer Steps Installation', 'category': stairs_cat, 'location': 'Mardan'},
        
        # Floors (20 images)
        {'file': 'floors/gallery10.jpg', 'title': 'Premium Marble Flooring', 'category': floors_cat, 'location': 'Faisalabad'},
        {'file': 'floors/gallery11.jpg', 'title': 'Luxury Floor Installation', 'category': floors_cat, 'location': 'Lahore'},
        {'file': 'floors/gallery12.jpg', 'title': 'Modern Floor Design', 'category': floors_cat, 'location': 'Karachi'},
        {'file': 'floors/gallery13.jpg', 'title': 'Elegant Granite Flooring', 'category': floors_cat, 'location': 'Islamabad'},
        {'file': 'floors/gallery14.jpg', 'title': 'Designer Floor Pattern', 'category': floors_cat, 'location': 'Faisalabad'},
        {'file': 'floors/gallery15.jpg', 'title': 'Contemporary Flooring', 'category': floors_cat, 'location': 'Lahore'},
        {'file': 'floors/gallery25.jpg', 'title': 'Marble Floor Masterpiece', 'category': floors_cat, 'location': 'Multan'},
        {'file': 'floors/gallery31.jpg', 'title': 'Luxury Marble Installation', 'category': floors_cat, 'location': 'Rawalpindi'},
        {'file': 'floors/gallery32.jpg', 'title': 'Premium Floor Finishing', 'category': floors_cat, 'location': 'Gujranwala'},
        {'file': 'floors/gallery37.jpg', 'title': 'Executive Floor Design', 'category': floors_cat, 'location': 'Sialkot'},
        {'file': 'floors/gallery38.jpg', 'title': 'Granite Floor Pattern', 'category': floors_cat, 'location': 'Peshawar'},
        {'file': 'floors/gallery4.jpg', 'title': 'Modern Marble Flooring', 'category': floors_cat, 'location': 'Quetta'},
        {'file': 'floors/gallery42.jpg', 'title': 'Elegant Floor Installation', 'category': floors_cat, 'location': 'Hyderabad'},
        {'file': 'floors/gallery44.jpg', 'title': 'Designer Marble Floor', 'category': floors_cat, 'location': 'Sargodha'},
        {'file': 'floors/gallery46.jpg', 'title': 'Premium Granite Flooring', 'category': floors_cat, 'location': 'Bahawalpur'},
        {'file': 'floors/gallery57.jpg', 'title': 'Luxury Floor Project', 'category': floors_cat, 'location': 'Sukkur'},
        {'file': 'floors/gallery6.jpg', 'title': 'Contemporary Floor Design', 'category': floors_cat, 'location': 'Larkana'},
        {'file': 'floors/gallery64.jpg', 'title': 'Marble Floor Excellence', 'category': floors_cat, 'location': 'Mardan'},
        {'file': 'floors/gallery8.jpg', 'title': 'Executive Flooring Work', 'category': floors_cat, 'location': 'Chiniot'},
        {'file': 'floors/gallery9.jpg', 'title': 'Premium Floor Craftsmanship', 'category': floors_cat, 'location': 'Sahiwal'},
        
        # Mosaic (12 images)
        {'file': 'mosaic/gallery17.jpg', 'title': 'Artistic Mosaic Design', 'category': mosaic_cat, 'location': 'Faisalabad'},
        {'file': 'mosaic/gallery19.jpg', 'title': 'Decorative Mosaic Pattern', 'category': mosaic_cat, 'location': 'Lahore'},
        {'file': 'mosaic/gallery20.jpg', 'title': 'Premium Mosaic Work', 'category': mosaic_cat, 'location': 'Karachi'},
        {'file': 'mosaic/gallery21.jpg', 'title': 'Elegant Mosaic Installation', 'category': mosaic_cat, 'location': 'Islamabad'},
        {'file': 'mosaic/gallery22.jpg', 'title': 'Contemporary Mosaic Art', 'category': mosaic_cat, 'location': 'Faisalabad'},
        {'file': 'mosaic/gallery23.jpg', 'title': 'Designer Mosaic Pattern', 'category': mosaic_cat, 'location': 'Lahore'},
        {'file': 'mosaic/gallery24.jpg', 'title': 'Luxury Mosaic Design', 'category': mosaic_cat, 'location': 'Multan'},
        {'file': 'mosaic/gallery29.jpg', 'title': 'Artistic Mosaic Creation', 'category': mosaic_cat, 'location': 'Rawalpindi'},
        {'file': 'mosaic/gallery30.jpg', 'title': 'Premium Mosaic Artwork', 'category': mosaic_cat, 'location': 'Gujranwala'},
        {'file': 'mosaic/gallery36.jpg', 'title': 'Decorative Mosaic Project', 'category': mosaic_cat, 'location': 'Sialkot'},
        {'file': 'mosaic/gallery40.jpg', 'title': 'Modern Mosaic Installation', 'category': mosaic_cat, 'location': 'Peshawar'},
        {'file': 'mosaic/gallery63.jpg', 'title': 'Executive Mosaic Design', 'category': mosaic_cat, 'location': 'Quetta'},
        
        # Others (13 images)
        {'file': 'others/gallery1.jpg', 'title': 'Custom Stone Installation', 'category': others_cat, 'location': 'Faisalabad'},
        {'file': 'others/gallery18.jpg', 'title': 'Special Project Design', 'category': others_cat, 'location': 'Lahore'},
        {'file': 'others/gallery2.jpg', 'title': 'Unique Marble Work', 'category': others_cat, 'location': 'Karachi'},
        {'file': 'others/gallery26.jpg', 'title': 'Designer Stone Project', 'category': others_cat, 'location': 'Islamabad'},
        {'file': 'others/gallery27.jpg', 'title': 'Premium Custom Work', 'category': others_cat, 'location': 'Faisalabad'},
        {'file': 'others/gallery28.jpg', 'title': 'Elegant Stone Installation', 'category': others_cat, 'location': 'Lahore'},
        {'file': 'others/gallery3.jpg', 'title': 'Luxury Custom Design', 'category': others_cat, 'location': 'Multan'},
        {'file': 'others/gallery43.jpg', 'title': 'Executive Stone Work', 'category': others_cat, 'location': 'Rawalpindi'},
        {'file': 'others/gallery45.jpg', 'title': 'Contemporary Installation', 'category': others_cat, 'location': 'Gujranwala'},
        {'file': 'others/gallery50.jpg', 'title': 'Artistic Stone Project', 'category': others_cat, 'location': 'Sialkot'},
        {'file': 'others/gallery51.jpg', 'title': 'Designer Custom Work', 'category': others_cat, 'location': 'Peshawar'},
        {'file': 'others/gallery58.jpg', 'title': 'Premium Stone Installation', 'category': others_cat, 'location': 'Quetta'},
        {'file': 'others/gallery61.jpg', 'title': 'Luxury Custom Project', 'category': others_cat, 'location': 'Hyderabad'},
    ]
    
    print(f"Starting upload to Azure Blob Storage...")
    print(f"Container: {AZURE_CONTAINER}")
    print(f"Account: {AZURE_ACCOUNT_NAME}")
    
    uploaded_count = 0
    
    for mapping in image_mappings:
        try:
            # Check if image already exists in database
            if GalleryImage.objects.filter(title=mapping['title']).exists():
                print(f"⏭️  Skipping {mapping['title']} - already exists in database")
                continue
            
            # Full path to local image
            local_image_path = frontend_assets / mapping['file']
            
            if not local_image_path.exists():
                print(f"❌ Local image not found: {local_image_path}")
                continue
            
            # Upload to Azure Blob Storage
            blob_name = f"gallery/{local_image_path.name}"
            blob_client = blob_service_client.get_blob_client(
                container=AZURE_CONTAINER, 
                blob=blob_name
            )
            
            print(f"📤 Uploading {local_image_path.name}...")
            
            with open(local_image_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            
            # Create database entry
            gallery_image = GalleryImage.objects.create(
                title=mapping['title'],
                image=blob_name,  # This will be the path in Azure
                category=mapping['category'],
                project_location=mapping['location'],
                description=f"Professional {mapping['category'].name.lower()} installation"
            )
            
            print(f"✅ Successfully uploaded and created: {mapping['title']}")
            uploaded_count += 1
            
        except Exception as e:
            print(f"❌ Error processing {mapping['title']}: {str(e)}")
    
    print(f"\n🎉 Upload complete! Uploaded {uploaded_count} images to Azure Blob Storage and database.")
    print(f"📊 Total database images: {GalleryImage.objects.count()}")

if __name__ == "__main__":
    upload_images_to_azure()
