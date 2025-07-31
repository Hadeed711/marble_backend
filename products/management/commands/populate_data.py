"""
Django management command to populate the database with initial data
for Sundar Marbles website including categories, products, gallery, and contact info.
"""

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone
from products.models import Category, Product
from gallery.models import GalleryCategory, GalleryImage
from contact.models import ContactInfo, ContactMessage
import requests
from datetime import date


class Command(BaseCommand):
    help = 'Populate database with initial data for Sundar Marbles'

    def handle(self, *args, **options):
        self.stdout.write('Starting database population...')
        
        # Create Product Categories
        self.create_product_categories()
        
        # Create Gallery Categories
        self.create_gallery_categories()
        
        # Create Contact Information
        self.create_contact_info()
        
        # Create Sample Products
        self.create_sample_products()
        
        # Create Sample Gallery Images
        self.create_sample_gallery()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with initial data!')
        )

    def create_product_categories(self):
        """Create product categories"""
        categories = [
            {
                'name': 'Marble',
                'description': 'Premium quality marble stones for flooring, walls, and decorative purposes.'
            },
            {
                'name': 'Granite',
                'description': 'Durable granite stones perfect for kitchen countertops and heavy-duty applications.'
            },
            {
                'name': 'Floor Tiles',
                'description': 'Beautiful floor tiles in various designs and sizes.'
            },
            {
                'name': 'Wall Tiles',
                'description': 'Elegant wall tiles for interior and exterior decoration.'
            },
            {
                'name': 'Mosaic',
                'description': 'Artistic mosaic tiles for decorative patterns and designs.'
            },
            {
                'name': 'Onyx',
                'description': 'Luxurious onyx stones for premium interior designs.'
            }
        ]
        
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(f'Created product category: {category.name}')
            else:
                self.stdout.write(f'Product category already exists: {category.name}')

    def create_gallery_categories(self):
        """Create gallery categories"""
        categories = [
            {
                'name': 'Stairs',
                'description': 'Beautiful marble and granite staircase installations',
                'order': 1
            },
            {
                'name': 'Floors',
                'description': 'Stunning floor installations in marble and granite',
                'order': 2
            },
            {
                'name': 'Kitchen Countertops',
                'description': 'Premium granite and marble kitchen countertops',
                'order': 3
            },
            {
                'name': 'Bathroom',
                'description': 'Elegant bathroom marble and tile work',
                'order': 4
            },
            {
                'name': 'Wall Cladding',
                'description': 'Decorative wall cladding and panels',
                'order': 5
            },
            {
                'name': 'Mosaic Work',
                'description': 'Artistic mosaic patterns and designs',
                'order': 6
            },
            {
                'name': 'Commercial Projects',
                'description': 'Large scale commercial marble installations',
                'order': 7
            }
        ]
        
        for cat_data in categories:
            category, created = GalleryCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'order': cat_data['order']
                }
            )
            if created:
                self.stdout.write(f'Created gallery category: {category.name}')
            else:
                self.stdout.write(f'Gallery category already exists: {category.name}')

    def create_contact_info(self):
        """Create contact information"""
        contact_info, created = ContactInfo.objects.get_or_create(
            company_name='Sundar Marbles & Granite',
            defaults={
                'address': 'Chakki Stop, New Green Town, Millat Road',
                'city': 'Faisalabad',
                'postal_code': '38000',
                'country': 'Pakistan',
                'primary_phone': '041-8816900',
                'secondary_phone': '0300-6641727',
                'whatsapp_number': '+923006641727',
                'email': 'info@sundarmarbles.com',
                'website': 'https://www.sundarmarbles.live',
                'business_hours': 'Monday - Saturday: 9:00 AM - 6:00 PM',
                'facebook_url': 'https://facebook.com/sundarmarbles',
                'instagram_url': 'https://instagram.com/sundarmarbles',
                'youtube_url': 'https://youtube.com/@sundarmarbles',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write('Created contact information')
        else:
            self.stdout.write('Contact information already exists')

    def create_sample_products(self):
        """Create sample products"""
        products_data = [
            {
                'name': 'Carrara White Marble',
                'description': 'Premium Italian Carrara white marble, perfect for luxury interiors',
                'category': 'Marble',
                'price': 15000.00,
                'origin': 'Italy',
                'finish': 'Polished',
                'thickness': '18mm'
            },
            {
                'name': 'Black Galaxy Granite',
                'description': 'Stunning black granite with gold speckles, ideal for countertops',
                'category': 'Granite',
                'price': 12000.00,
                'origin': 'India',
                'finish': 'Polished',
                'thickness': '20mm'
            },
            {
                'name': 'Botticino Marble',
                'description': 'Classic beige marble with subtle veining patterns',
                'category': 'Marble',
                'price': 8000.00,
                'origin': 'Italy',
                'finish': 'Honed',
                'thickness': '18mm'
            },
            {
                'name': 'Porcelain Floor Tiles',
                'description': 'High-quality porcelain tiles suitable for heavy traffic areas',
                'category': 'Floor Tiles',
                'price': 2500.00,
                'origin': 'Pakistan',
                'finish': 'Matt',
                'thickness': '10mm'
            },
            {
                'name': 'Green Onyx',
                'description': 'Beautiful translucent green onyx for decorative applications',
                'category': 'Onyx',
                'price': 20000.00,
                'origin': 'Pakistan',
                'finish': 'Polished',
                'thickness': '15mm'
            }
        ]
        
        for product_data in products_data:
            try:
                category = Category.objects.get(name=product_data['category'])
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults={
                        'description': product_data['description'],
                        'category': category,
                        'price': product_data['price'],
                        'origin': product_data['origin'],
                        'finish': product_data['finish'],
                        'thickness': product_data['thickness'],
                        'is_active': True,
                        'is_featured': True
                    }
                )
                
                if created:
                    self.stdout.write(f'Created product: {product.name}')
                else:
                    self.stdout.write(f'Product already exists: {product.name}')
                    
            except Category.DoesNotExist:
                self.stdout.write(f'Category not found: {product_data["category"]}')

    def create_sample_gallery(self):
        """Create sample gallery images"""
        gallery_data = [
            {
                'title': 'Elegant Marble Staircase',
                'description': 'Beautiful white marble staircase with brass railings',
                'category': 'Stairs',
                'project_location': 'DHA Lahore',
                'is_featured': True
            },
            {
                'title': 'Modern Kitchen Countertop',
                'description': 'Black granite countertop with undermount sink',
                'category': 'Kitchen Countertops',
                'project_location': 'Faisalabad',
                'is_featured': True
            },
            {
                'title': 'Luxury Marble Floor',
                'description': 'Premium marble flooring in living room',
                'category': 'Floors',
                'project_location': 'Islamabad',
                'is_featured': True
            },
            {
                'title': 'Bathroom Marble Installation',
                'description': 'Complete bathroom renovation with marble tiles',
                'category': 'Bathroom',
                'project_location': 'Karachi',
                'is_featured': False
            },
            {
                'title': 'Decorative Wall Cladding',
                'description': 'Artistic marble wall cladding in office lobby',
                'category': 'Wall Cladding',
                'project_location': 'Lahore',
                'is_featured': True
            }
        ]
        
        for gallery_item in gallery_data:
            try:
                category = GalleryCategory.objects.get(name=gallery_item['category'])
                gallery_image, created = GalleryImage.objects.get_or_create(
                    title=gallery_item['title'],
                    defaults={
                        'description': gallery_item['description'],
                        'category': category,
                        'project_location': gallery_item['project_location'],
                        'is_featured': gallery_item['is_featured'],
                        'is_active': True,
                        'completion_date': date.today()
                    }
                )
                
                if created:
                    self.stdout.write(f'Created gallery item: {gallery_image.title}')
                else:
                    self.stdout.write(f'Gallery item already exists: {gallery_image.title}')
                    
            except GalleryCategory.DoesNotExist:
                self.stdout.write(f'Gallery category not found: {gallery_item["category"]}')
