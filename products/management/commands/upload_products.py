import os
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Upload product images from frontend assets to database with Azure Blob Storage'

    def handle(self, *args, **options):
        # Create categories first
        marble_category, created = Category.objects.get_or_create(
            name='Marble',
            defaults={'slug': 'marble', 'description': 'Premium marble products'}
        )
        granite_category, created = Category.objects.get_or_create(
            name='Granite',
            defaults={'slug': 'granite', 'description': 'High-quality granite products'}
        )
        
        self.stdout.write(f"✅ Categories created/found: {marble_category.name}, {granite_category.name}")

        # Product data mapping (name -> category, price, description)
        products_data = {
            'black_gold.jpg': {
                'name': 'Black Gold Marble',
                'category': marble_category,
                'price': Decimal('2500.00'),
                'description': 'Luxurious black marble with golden veining, perfect for premium installations.',
                'origin': 'Italy',
                'finish': 'Polished',
                'thickness': '18mm'
            },
            'booti_seena.png': {
                'name': 'Booti Seena Granite',
                'category': granite_category,
                'price': Decimal('1800.00'),
                'description': 'Traditional granite with unique patterns, ideal for flooring and countertops.',
                'origin': 'Pakistan',
                'finish': 'Honed',
                'thickness': '20mm'
            },
            'jet_black.png': {
                'name': 'Jet Black Marble',
                'category': marble_category,
                'price': Decimal('3200.00'),
                'description': 'Pure jet black marble for modern and elegant designs.',
                'origin': 'China',
                'finish': 'Polished',
                'thickness': '18mm'
            },
            'star_black.jpg': {
                'name': 'Star Black Marble',
                'category': marble_category,
                'price': Decimal('2800.00'),
                'description': 'Black marble with star-like patterns, adds sophistication to any space.',
                'origin': 'India',
                'finish': 'Polished',
                'thickness': '18mm'
            },
            'sunny_grey.jpg': {
                'name': 'Sunny Grey Marble',
                'category': marble_category,
                'price': Decimal('2200.00'),
                'description': 'Light grey marble with subtle patterns, perfect for contemporary designs.',
                'origin': 'Turkey',
                'finish': 'Brushed',
                'thickness': '20mm'
            },
            'sunny_white.jpg': {
                'name': 'Sunny White Marble',
                'category': marble_category,
                'price': Decimal('2600.00'),
                'description': 'Pure white marble with delicate veining, ideal for luxury interiors.',
                'origin': 'Greece',
                'finish': 'Polished',
                'thickness': '18mm'
            },
            'taweera.png': {
                'name': 'Taweera Granite',
                'category': granite_category,
                'price': Decimal('1600.00'),
                'description': 'Local granite with excellent durability and unique color patterns.',
                'origin': 'Pakistan',
                'finish': 'Flamed',
                'thickness': '25mm'
            },
            'tropical_grey.png': {
                'name': 'Tropical Grey Granite',
                'category': granite_category,
                'price': Decimal('1900.00'),
                'description': 'Grey granite with tropical patterns, perfect for outdoor applications.',
                'origin': 'Brazil',
                'finish': 'Honed',
                'thickness': '20mm'
            }
        }

        # Base path to frontend assets
        frontend_assets_path = r'f:\development\sundar_marbles\marble-tiles-site\src\assets\products'
        
        uploaded_count = 0
        
        for filename, product_info in products_data.items():
            # Check if product already exists
            if Product.objects.filter(name=product_info['name']).exists():
                self.stdout.write(f"⚠️  Product '{product_info['name']}' already exists, skipping...")
                continue
            
            # Full path to image file
            image_path = os.path.join(frontend_assets_path, filename)
            
            if not os.path.exists(image_path):
                self.stdout.write(f"❌ Image file not found: {image_path}")
                continue
            
            try:
                # Read the image file
                with open(image_path, 'rb') as img_file:
                    image_content = img_file.read()
                
                # Create Django file object
                django_file = ContentFile(image_content, name=filename)
                
                # Create the product
                product = Product.objects.create(
                    name=product_info['name'],
                    description=product_info['description'],
                    category=product_info['category'],
                    price=product_info['price'],
                    origin=product_info['origin'],
                    finish=product_info['finish'],
                    thickness=product_info['thickness'],
                    is_active=True,
                    is_featured=True,  # Make all uploaded products featured
                    image=django_file  # This will automatically upload to Azure Blob Storage
                )
                
                uploaded_count += 1
                blob_url = product.image.url if product.image else 'No URL'
                
                self.stdout.write(
                    f"✅ Created product: {product.name} ({product.category.name})"
                )
                self.stdout.write(f"   💰 Price: PKR {product.price}")
                self.stdout.write(f"   🌐 Blob URL: {blob_url}")
                self.stdout.write(f"   📁 File: {filename}")
                self.stdout.write("   " + "-" * 50)
                
            except Exception as e:
                self.stdout.write(f"❌ Error creating product '{product_info['name']}': {str(e)}")
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(f"🎉 UPLOAD COMPLETE!")
        self.stdout.write(f"📊 Total products uploaded: {uploaded_count}/8")
        self.stdout.write(f"🗄️  Database: PostgreSQL (Neon)")
        self.stdout.write(f"☁️  Images stored: Azure Blob Storage")
        self.stdout.write(f"🌐 Admin panel: https://sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net/admin/")
        self.stdout.write("=" * 60)
