"""
Management command to fix product image URLs to point to Azure Blob Storage
"""
from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Fix product image URLs to point to Azure Blob Storage'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Checking product images...'))
        
        products = Product.objects.all()
        azure_base = 'https://sundarmarbles.blob.core.windows.net/media/products/'
        
        for product in products:
            if product.image:
                current_path = str(product.image)
                self.stdout.write(f'Product: {product.name}')
                self.stdout.write(f'  Current image path: {current_path}')
                
                # Check if it needs to be updated to Azure URL
                if not current_path.startswith('https://'):
                    # It's a relative path, needs Azure URL
                    if current_path.startswith('products/'):
                        azure_url = f'{azure_base}{current_path[9:]}'  # Remove 'products/' prefix
                    else:
                        azure_url = f'{azure_base}{current_path}'
                    
                    self.stdout.write(f'  Azure URL: {azure_url}')
                else:
                    self.stdout.write(f'  Already full URL: {current_path}')
                
                self.stdout.write('---')
        
        self.stdout.write(self.style.SUCCESS('✅ Product image check complete'))
