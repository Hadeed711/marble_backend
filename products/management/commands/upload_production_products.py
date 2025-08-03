"""
Management command to upload all product images to the production database
This should be run on the Azure production server
"""

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Category, Product
from decimal import Decimal
import requests
import os


class Command(BaseCommand):
    help = 'Upload all products with images to production database'

    def handle(self, *args, **options):
        self.stdout.write("🚀 PRODUCTION UPLOAD STARTED")
        self.stdout.write("=" * 50)
        
        # Create categories first
        marble_category, created = Category.objects.get_or_create(
            name='Marble',
            defaults={'slug': 'marble', 'description': 'Premium marble products'}
        )
        granite_category, created = Category.objects.get_or_create(
            name='Granite', 
            defaults={'slug': 'granite', 'description': 'High-quality granite products'}
        )
        
        self.stdout.write(f"✅ Categories ready: {marble_category.name}, {granite_category.name}")

        # Product data with direct image URLs (since we can't access local files on Azure)
        products_data = [
            {
                'name': 'Black Gold Marble',
                'category': marble_category,
                'price': Decimal('12000.00'),
                'description': 'Luxurious black marble with golden veining, perfect for premium installations.',
                'origin': 'Italy',
                'finish': 'Polished',
                'thickness': '18mm',
                # We'll use a placeholder or default image since we can't upload local files directly
                'image_url': None  # Will be handled manually in admin
            },
            {
                'name': 'Star Black Marble',
                'category': marble_category,
                'price': Decimal('8500.00'),
                'description': 'Black marble with star-like patterns, adds sophistication to any space.',
                'origin': 'India',
                'finish': 'Polished',
                'thickness': '18mm',
                'image_url': None
            },
            {
                'name': 'Jet Black Marble',
                'category': marble_category,
                'price': Decimal('7800.00'),
                'description': 'Pure jet black marble for modern and elegant designs.',
                'origin': 'China',
                'finish': 'Polished',
                'thickness': '18mm',
                'image_url': None
            },
            {
                'name': 'Sunny White Marble',
                'category': marble_category,
                'price': Decimal('6800.00'),
                'description': 'Pure white marble with delicate veining, ideal for luxury interiors.',
                'origin': 'Greece',
                'finish': 'Polished',
                'thickness': '18mm',
                'image_url': None
            },
            {
                'name': 'Sunny Grey Marble',
                'category': marble_category,
                'price': Decimal('7200.00'),
                'description': 'Light grey marble with subtle patterns, perfect for contemporary designs.',
                'origin': 'Turkey',
                'finish': 'Brushed',
                'thickness': '20mm',
                'image_url': None
            },
            {
                'name': 'Taweera Granite',
                'category': granite_category,
                'price': Decimal('9200.00'),
                'description': 'Local granite with excellent durability and unique color patterns.',
                'origin': 'Pakistan',
                'finish': 'Flamed',
                'thickness': '25mm',
                'image_url': None
            },
            {
                'name': 'Booti Seena Granite',
                'category': granite_category,
                'price': Decimal('8200.00'),
                'description': 'Traditional granite with unique patterns, ideal for flooring and countertops.',
                'origin': 'Pakistan',
                'finish': 'Honed',
                'thickness': '20mm',
                'image_url': None
            },
            {
                'name': 'Tropical Grey Granite',
                'category': granite_category,
                'price': Decimal('10500.00'),
                'description': 'Grey granite with tropical patterns, perfect for outdoor applications.',
                'origin': 'Brazil',
                'finish': 'Honed',
                'thickness': '20mm',
                'image_url': None
            }
        ]

        uploaded_count = 0
        
        for product_info in products_data:
            # Check if product already exists
            if Product.objects.filter(name=product_info['name']).exists():
                self.stdout.write(f"⚠️  Product '{product_info['name']}' already exists, skipping...")
                continue
            
            try:
                # Create the product without image first
                product = Product.objects.create(
                    name=product_info['name'],
                    description=product_info['description'],
                    category=product_info['category'],
                    price=product_info['price'],
                    origin=product_info['origin'],
                    finish=product_info['finish'],
                    thickness=product_info['thickness'],
                    is_active=True,
                    is_featured=True
                    # Note: Image will be uploaded manually through admin panel
                )
                
                uploaded_count += 1
                
                self.stdout.write(f"✅ Created product: {product.name} ({product.category.name})")
                self.stdout.write(f"   💰 Price: PKR {product.price}")
                self.stdout.write(f"   📝 ID: {product.id}")
                self.stdout.write("   " + "-" * 40)
                
            except Exception as e:
                self.stdout.write(f"❌ Error creating product '{product_info['name']}': {str(e)}")
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(f"🎉 PRODUCTION UPLOAD COMPLETE!")
        self.stdout.write(f"📊 Total products created: {uploaded_count}/8")
        self.stdout.write(f"🗄️  Database: PostgreSQL (Neon)")
        self.stdout.write(f"📝 Next Steps:")
        self.stdout.write(f"   1. Go to admin panel: /admin/products/product/")
        self.stdout.write(f"   2. Edit each product to upload images")
        self.stdout.write(f"   3. Images will automatically upload to Azure Blob Storage")
        self.stdout.write("=" * 60)
