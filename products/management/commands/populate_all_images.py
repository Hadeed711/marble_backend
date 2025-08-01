import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Product, Category as ProductCategory
from gallery.models import GalleryImage, GalleryCategory

class Command(BaseCommand):
    help = 'Populate database with all images from assets folder'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate all images...')
        
        # Create media directories if they don't exist
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'products'), exist_ok=True)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'gallery'), exist_ok=True)
        
        # Populate products
        self.populate_products()
        
        # Populate gallery
        self.populate_gallery()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated all images!'))

    def populate_products(self):
        self.stdout.write('Populating products...')
        
        # Create product categories
        marble_category, created = ProductCategory.objects.get_or_create(
            name="Marble",
            defaults={'slug': 'marble', 'description': 'Premium marble collection'}
        )
        
        granite_category, created = ProductCategory.objects.get_or_create(
            name="Granite", 
            defaults={'slug': 'granite', 'description': 'Durable granite collection'}
        )
        
        # Product data with image files
        products_data = [
            {
                'name': 'Black Gold Marble',
                'description': 'Premium black marble with gold veining for luxury spaces',
                'price': 12000,
                'category': marble_category,
                'image_file': 'black_gold.jpg',
                'finish': 'Polished',
                'thickness': '20mm',
                'origin': 'Pakistan'
            },
            {
                'name': 'Star Black Marble',
                'description': 'Elegant black marble with star patterns',
                'price': 8500,
                'category': marble_category,
                'image_file': 'star_black.jpg',
                'finish': 'Polished',
                'thickness': '18mm',
                'origin': 'Pakistan'
            },
            {
                'name': 'Taweera Granite',
                'description': 'Durable granite with natural patterns',
                'price': 9200,
                'category': granite_category,
                'image_file': 'taweera.png',
                'finish': 'Polished',
                'thickness': '20mm',
                'origin': 'Pakistan'
            },
            {
                'name': 'Jet Black Marble',
                'description': 'Deep black marble for modern designs',
                'price': 7800,
                'category': marble_category,
                'image_file': 'jet_black.png',
                'finish': 'Polished',
                'thickness': '18mm',
                'origin': 'Pakistan'
            },
            {
                'name': 'Tropical Grey Granite',
                'description': 'Grey granite with tropical patterns',
                'price': 10500,
                'category': granite_category,
                'image_file': 'tropical_grey.png',
                'finish': 'Polished',
                'thickness': '20mm',
                'origin': 'Pakistan'
            },
            {
                'name': 'Booti Seena Granite',
                'description': 'Classic granite with speckled finish',
                'price': 8200,
                'category': granite_category,
                'image_file': 'booti_seena.png',
                'finish': 'Polished',
                'thickness': '18mm',
                'origin': 'Pakistan'
            },
            {
                'name': 'Sunny White Marble',
                'description': 'Bright white marble for luxury spaces',
                'price': 6800,
                'category': marble_category,
                'image_file': 'sunny_white.jpg',
                'finish': 'Polished',
                'thickness': '20mm',
                'origin': 'Pakistan'
            },
            {
                'name': 'Sunny Grey Marble',
                'description': 'Sophisticated grey marble with subtle veining',
                'price': 7200,
                'category': marble_category,
                'image_file': 'sunny_grey.jpg',
                'finish': 'Polished',
                'thickness': '18mm',
                'origin': 'Pakistan'
            },
        ]
        
        # Source path for product images
        source_dir = r'f:\development\sundar_marbles\marble-tiles-site\src\assets\products'
        
        for product_data in products_data:
            image_file = product_data.pop('image_file')
            source_path = os.path.join(source_dir, image_file)
            
            if os.path.exists(source_path):
                # Copy image to media directory
                dest_path = os.path.join(settings.MEDIA_ROOT, 'products', image_file)
                shutil.copy2(source_path, dest_path)
                
                # Create or update product
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults={
                        **product_data,
                        'image': f'products/{image_file}',
                        'is_featured': True,
                        'is_active': True
                    }
                )
                
                if created:
                    self.stdout.write(f'  Created product: {product.name}')
                else:
                    # Update existing product
                    for key, value in product_data.items():
                        setattr(product, key, value)
                    product.image = f'products/{image_file}'
                    product.save()
                    self.stdout.write(f'  Updated product: {product.name}')
            else:
                self.stdout.write(f'  Warning: Image not found: {source_path}')

    def populate_gallery(self):
        self.stdout.write('Populating gallery...')
        
        # Create gallery categories
        stairs_category, created = GalleryCategory.objects.get_or_create(
            name="Stairs",
            defaults={'slug': 'stairs', 'description': 'Beautiful staircase installations'}
        )
        
        floors_category, created = GalleryCategory.objects.get_or_create(
            name="Floors", 
            defaults={'slug': 'floors', 'description': 'Premium flooring projects'}
        )
        
        mosaic_category, created = GalleryCategory.objects.get_or_create(
            name="Mosaic",
            defaults={'slug': 'mosaic', 'description': 'Artistic mosaic designs'}
        )
        
        others_category, created = GalleryCategory.objects.get_or_create(
            name="Others",
            defaults={'slug': 'others', 'description': 'Custom and special projects'}
        )
        
        # Gallery data structure
        gallery_data = {
            'stairs': {
                'category': stairs_category,
                'images': [
                    'gallery16.jpg', 'gallery33.jpg', 'gallery34.jpg', 'gallery35.jpg',
                    'gallery39.jpg', 'gallery41.jpg', 'gallery47.jpg', 'gallery48.jpg',
                    'gallery49.jpg', 'gallery5.jpg', 'gallery52.jpg', 'gallery53.jpg',
                    'gallery54.jpg', 'gallery55.jpg', 'gallery56.jpg', 'gallery65.jpg',
                    'gallery66.jpg', 'gallery7.jpg'
                ]
            },
            'floors': {
                'category': floors_category,
                'images': [
                    'gallery10.jpg', 'gallery11.jpg', 'gallery12.jpg', 'gallery13.jpg',
                    'gallery14.jpg', 'gallery15.jpg', 'gallery25.jpg', 'gallery31.jpg',
                    'gallery32.jpg', 'gallery37.jpg', 'gallery38.jpg', 'gallery4.jpg',
                    'gallery42.jpg', 'gallery44.jpg', 'gallery46.jpg', 'gallery57.jpg',
                    'gallery6.jpg', 'gallery64.jpg', 'gallery8.jpg', 'gallery9.jpg'
                ]
            },
            'mosaic': {
                'category': mosaic_category,
                'images': [
                    'gallery17.jpg', 'gallery19.jpg', 'gallery20.jpg', 'gallery21.jpg',
                    'gallery22.jpg', 'gallery23.jpg', 'gallery24.jpg', 'gallery29.jpg',
                    'gallery30.jpg', 'gallery36.jpg', 'gallery40.jpg', 'gallery63.jpg'
                ]
            },
            'others': {
                'category': others_category,
                'images': [
                    'gallery1.jpg', 'gallery18.jpg', 'gallery2.jpg', 'gallery26.jpg',
                    'gallery27.jpg', 'gallery28.jpg', 'gallery3.jpg', 'gallery43.jpg',
                    'gallery45.jpg', 'gallery50.jpg', 'gallery51.jpg', 'gallery58.jpg',
                    'gallery61.jpg'
                ]
            }
        }
        
        # Cities for project locations
        cities = ['Faisalabad', 'Lahore', 'Karachi', 'Islamabad', 'Multan', 'Rawalpindi', 
                 'Gujranwala', 'Sialkot', 'Peshawar', 'Quetta', 'Hyderabad', 'Sargodha',
                 'Bahawalpur', 'Sukkur', 'Larkana', 'Mardan', 'Chiniot', 'Sahiwal']
        
        for folder, data in gallery_data.items():
            source_dir = rf'f:\development\sundar_marbles\marble-tiles-site\src\assets\{folder}'
            category = data['category']
            
            for i, image_file in enumerate(data['images']):
                source_path = os.path.join(source_dir, image_file)
                
                if os.path.exists(source_path):
                    # Copy image to media directory
                    dest_path = os.path.join(settings.MEDIA_ROOT, 'gallery', image_file)
                    shutil.copy2(source_path, dest_path)
                    
                    # Generate title and description
                    if folder == 'stairs':
                        titles = ['Premium Marble Staircase', 'Elegant Curved Staircase', 'Modern Spiral Stairs', 
                                'Classic Marble Steps', 'Luxury Staircase Installation', 'Contemporary Stair Design']
                    elif folder == 'floors':
                        titles = ['Premium Marble Flooring', 'Luxury Floor Installation', 'Modern Floor Design',
                                'Elegant Granite Flooring', 'Designer Floor Pattern', 'Contemporary Flooring']
                    elif folder == 'mosaic':
                        titles = ['Artistic Mosaic Design', 'Decorative Mosaic Pattern', 'Premium Mosaic Work',
                                'Elegant Mosaic Installation', 'Contemporary Mosaic Art', 'Designer Mosaic Pattern']
                    else:
                        titles = ['Custom Stone Installation', 'Special Project Design', 'Unique Marble Work',
                                'Designer Stone Project', 'Premium Custom Work', 'Elegant Stone Installation']
                    
                    title = f"{titles[i % len(titles)]} {i+1}"
                    location = cities[i % len(cities)]
                    
                    # Create or update gallery image
                    gallery_image, created = GalleryImage.objects.get_or_create(
                        image=f'gallery/{image_file}',
                        defaults={
                            'title': title,
                            'description': f'Beautiful {folder} installation in {location}',
                            'category': category,
                            'project_location': location,
                            'is_featured': i < 3,  # Make first 3 images featured
                            'is_active': True
                        }
                    )
                    
                    if created:
                        self.stdout.write(f'  Created gallery image: {title}')
                    else:
                        self.stdout.write(f'  Gallery image already exists: {title}')
                else:
                    self.stdout.write(f'  Warning: Image not found: {source_path}')
