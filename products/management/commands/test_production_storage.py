from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import io
from PIL import Image
import requests


class Command(BaseCommand):
    help = 'Test production Azure Blob Storage connectivity and fix any issues'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Testing Production Azure Blob Storage...'))
        
        # Check storage configuration
        self.stdout.write(f"📡 Storage backend: {default_storage.__class__.__name__}")
        
        if hasattr(settings, 'AZURE_ACCOUNT_NAME'):
            self.stdout.write(f"☁️  Azure Account: {settings.AZURE_ACCOUNT_NAME}")
            self.stdout.write(f"📦 Azure Container: {getattr(settings, 'AZURE_CONTAINER', 'media')}")
            self.stdout.write(f"🌐 Media URL: {settings.MEDIA_URL}")
        else:
            self.stdout.write(self.style.ERROR('❌ Azure configuration not found!'))
            return
        
        try:
            # Test 1: Create a test image
            self.stdout.write('\n🧪 Test 1: Creating test image...')
            img = Image.new('RGB', (200, 200), color='blue')
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG', quality=95)
            img_io.seek(0)
            
            # Test 2: Upload to Azure Blob Storage
            self.stdout.write('📤 Test 2: Uploading to Azure Blob Storage...')
            test_file = ContentFile(img_io.getvalue(), name='test_production.jpg')
            file_path = default_storage.save('products/test_production.jpg', test_file)
            
            self.stdout.write(self.style.SUCCESS(f'✅ Upload successful: {file_path}'))
            
            # Test 3: Generate URL
            self.stdout.write('🔗 Test 3: Generating public URL...')
            file_url = default_storage.url(file_path)
            self.stdout.write(self.style.SUCCESS(f'✅ URL generated: {file_url}'))
            
            # Test 4: Verify URL accessibility
            self.stdout.write('🌐 Test 4: Testing URL accessibility...')
            response = requests.head(file_url, timeout=10)
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('✅ URL is publicly accessible'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  URL returned status: {response.status_code}'))
            
            # Test 5: File existence check
            self.stdout.write('📋 Test 5: Checking file existence...')
            exists = default_storage.exists(file_path)
            self.stdout.write(self.style.SUCCESS(f'✅ File exists: {exists}'))
            
            # Test 6: Clean up
            self.stdout.write('🧹 Test 6: Cleaning up test file...')
            default_storage.delete(file_path)
            self.stdout.write(self.style.SUCCESS('✅ Test file cleaned up'))
            
            # Success message
            self.stdout.write(self.style.SUCCESS('\n🎉 ALL TESTS PASSED!'))
            self.stdout.write(self.style.SUCCESS('✅ Azure Blob Storage is working correctly'))
            self.stdout.write(self.style.SUCCESS('✅ Admin panel should now work without errors'))
            self.stdout.write(self.style.SUCCESS('✅ Images will upload to: https://sundarmarbles.blob.core.windows.net/media/products/'))
            self.stdout.write(self.style.SUCCESS('✅ Products will render on: https://www.sundarmarbles.live/products'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Production test failed: {str(e)}'))
            
            # Detailed debugging
            self.stdout.write(self.style.WARNING('\n🔍 Debugging information:'))
            
            # Check environment variables
            from decouple import config
            self.stdout.write(f"AZURE_ACCOUNT_NAME: {'✅' if config('AZURE_ACCOUNT_NAME', default=None) else '❌ Missing'}")
            self.stdout.write(f"AZURE_ACCOUNT_KEY: {'✅' if config('AZURE_ACCOUNT_KEY', default=None) else '❌ Missing'}")
            self.stdout.write(f"AZURE_CONTAINER: {config('AZURE_CONTAINER', default='media')}")
            
            # Check STORAGES setting
            storages_config = getattr(settings, 'STORAGES', {})
            if storages_config:
                self.stdout.write(f"STORAGES config: ✅ Present")
                default_storage_backend = storages_config.get('default', {}).get('BACKEND', 'Not set')
                self.stdout.write(f"Default storage backend: {default_storage_backend}")
            else:
                self.stdout.write(f"STORAGES config: ❌ Missing (using legacy DEFAULT_FILE_STORAGE)")
            
            # Full error traceback
            import traceback
            self.stdout.write(self.style.ERROR(f'\nFull error details:\n{traceback.format_exc()}'))
            
            # Recommendations
            self.stdout.write(self.style.WARNING('\n💡 Recommendations:'))
            self.stdout.write('1. Check Azure App Service environment variables')
            self.stdout.write('2. Ensure Azure Storage Account has proper permissions')
            self.stdout.write('3. Verify CORS settings in Azure Storage Account')
            self.stdout.write('4. Check if Azure Storage Account allows blob access')
