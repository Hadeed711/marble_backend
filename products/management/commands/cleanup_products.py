from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Clean up products without images'

    def handle(self, *args, **options):
        # Find products without images
        products_without_images = Product.objects.filter(image='')
        
        self.stdout.write(f"Found {products_without_images.count()} products without images:")
        
        for product in products_without_images:
            self.stdout.write(f"  - ID {product.id}: {product.name}")
        
        if products_without_images.count() > 0:
            confirm = input("\nDelete these products? (y/N): ")
            if confirm.lower() == 'y':
                deleted_count = products_without_images.count()
                products_without_images.delete()
                self.stdout.write(f"✅ Deleted {deleted_count} products without images")
            else:
                self.stdout.write("❌ Cancelled deletion")
        else:
            self.stdout.write("✅ All products have images!")
