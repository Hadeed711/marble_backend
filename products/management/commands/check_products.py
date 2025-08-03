from django.core.management.base import BaseCommand
from products.models import Product, Category


class Command(BaseCommand):
    help = 'Check products and their images in database'

    def handle(self, *args, **options):
        products = Product.objects.all()
        categories = Category.objects.all()
        
        self.stdout.write(f"📊 CURRENT DATABASE STATUS")
        self.stdout.write("=" * 50)
        self.stdout.write(f"Categories: {categories.count()}")
        for cat in categories:
            self.stdout.write(f"  - {cat.name} ({cat.products.count()} products)")
        
        self.stdout.write(f"\nProducts: {products.count()}")
        self.stdout.write("-" * 50)
        
        for p in products:
            has_image = bool(p.image)
            image_url = p.image.url if p.image else "No image"
            self.stdout.write(f"ID {p.id}: {p.name}")
            self.stdout.write(f"  Category: {p.category.name}")
            self.stdout.write(f"  Image: {'✅' if has_image else '❌'} {image_url}")
            self.stdout.write(f"  Price: PKR {p.price}")
            self.stdout.write("")
