from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import io
from PIL import Image


class Command(BaseCommand):
    help = 'Test Azure Blob Storage connectivity and upload functionality'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing Azure Blob Storage...'))
        
        # Check storage configuration
        self.stdout.write(f"Storage backend: {default_storage.__class__.__name__}")
        
        if hasattr(settings, 'AZURE_ACCOUNT_NAME'):
            self.stdout.write(f"Azure Account: {settings.AZURE_ACCOUNT_NAME}")
            self.stdout.write(f"Azure Container: {getattr(settings, 'AZURE_CONTAINER', 'media')}")
            self.stdout.write(f"Media URL: {settings.MEDIA_URL}")
        
        try:
            # Create a test image
            img = Image.new('RGB', (100, 100), color='red')
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG')
            img_io.seek(0)
            
            # Test file upload
            test_file = ContentFile(img_io.getvalue(), name='test_image.jpg')
            file_path = default_storage.save('products/test_image.jpg', test_file)
            
            self.stdout.write(self.style.SUCCESS(f'✅ File uploaded successfully: {file_path}'))
            
            # Test file URL generation
            file_url = default_storage.url(file_path)
            self.stdout.write(self.style.SUCCESS(f'✅ File URL: {file_url}'))
            
            # Test file existence
            exists = default_storage.exists(file_path)
            self.stdout.write(self.style.SUCCESS(f'✅ File exists: {exists}'))
            
            # Clean up test file
            default_storage.delete(file_path)
            self.stdout.write(self.style.SUCCESS('✅ Test file cleaned up'))
            
            self.stdout.write(self.style.SUCCESS('\n🎉 Azure Blob Storage is working correctly!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Azure Blob Storage test failed: {str(e)}'))
            self.stdout.write(self.style.WARNING('\n🔍 Debugging information:'))
            
            # Debug information
            import traceback
            self.stdout.write(self.style.WARNING(f'Full error: {traceback.format_exc()}'))
            
            # Check environment variables
            from decouple import config
            self.stdout.write(f"AZURE_ACCOUNT_NAME env: {'✅' if config('AZURE_ACCOUNT_NAME', default=None) else '❌'}")
            self.stdout.write(f"AZURE_ACCOUNT_KEY env: {'✅' if config('AZURE_ACCOUNT_KEY', default=None) else '❌'}")
            self.stdout.write(f"AZURE_CONTAINER env: {config('AZURE_CONTAINER', default='media')}")
