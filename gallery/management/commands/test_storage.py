from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Test storage configuration and upload path'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🔍 STORAGE CONFIGURATION DIAGNOSIS'))
        self.stdout.write('=' * 50)
        
        # Check Django settings
        self.stdout.write(f"📊 Django Version: {settings.DEBUG and 'Development' or 'Production'}")
        self.stdout.write(f"🔧 DEBUG Mode: {settings.DEBUG}")
        
        # Check storage backend
        self.stdout.write(f"💾 Default Storage Backend: {default_storage.__class__}")
        self.stdout.write(f"📂 Storage Location: {default_storage.location if hasattr(default_storage, 'location') else 'N/A'}")
        
        # Check STORAGES configuration
        if hasattr(settings, 'STORAGES'):
            self.stdout.write(f"⚙️  STORAGES (Django 4.2+): {settings.STORAGES}")
        else:
            self.stdout.write("⚠️  No STORAGES setting found")
            
        # Check legacy DEFAULT_FILE_STORAGE
        if hasattr(settings, 'DEFAULT_FILE_STORAGE'):
            self.stdout.write(f"🔄 DEFAULT_FILE_STORAGE (Legacy): {settings.DEFAULT_FILE_STORAGE}")
        else:
            self.stdout.write("ℹ️  No DEFAULT_FILE_STORAGE setting found")
            
        # Check Azure settings
        azure_settings = {}
        for attr in ['AZURE_ACCOUNT_NAME', 'AZURE_ACCOUNT_KEY', 'AZURE_CONTAINER', 'AZURE_CUSTOM_DOMAIN']:
            if hasattr(settings, attr):
                if 'KEY' in attr:
                    azure_settings[attr] = f"***{getattr(settings, attr)[-4:] if getattr(settings, attr) else 'NOT SET'}***"
                else:
                    azure_settings[attr] = getattr(settings, attr)
            else:
                azure_settings[attr] = 'NOT SET'
                
        self.stdout.write("☁️  Azure Configuration:")
        for key, value in azure_settings.items():
            self.stdout.write(f"   {key}: {value}")
            
        # Check media settings
        self.stdout.write(f"🌐 MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'NOT SET')}")
        if hasattr(settings, 'MEDIA_ROOT'):
            self.stdout.write(f"📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
            
        # Test storage functionality
        self.stdout.write('\n🧪 TESTING STORAGE FUNCTIONALITY')
        self.stdout.write('=' * 50)
        
        try:
            # Test if we can save a file
            test_content = b"Test file for storage verification"
            test_path = "gallery/test_upload.txt"
            
            # Save test file
            saved_path = default_storage.save(test_path, test_content)
            self.stdout.write(f"✅ File saved successfully to: {saved_path}")
            
            # Check if file exists
            if default_storage.exists(saved_path):
                self.stdout.write(f"✅ File exists in storage")
                
                # Get file URL
                try:
                    file_url = default_storage.url(saved_path)
                    self.stdout.write(f"🔗 File URL: {file_url}")
                except Exception as e:
                    self.stdout.write(f"❌ Error getting file URL: {e}")
                
                # Clean up test file
                default_storage.delete(saved_path)
                self.stdout.write(f"🗑️  Test file cleaned up")
            else:
                self.stdout.write(f"❌ File does not exist in storage after save")
                
        except Exception as e:
            self.stdout.write(f"❌ Storage test failed: {e}")
            
        # Check installed apps
        self.stdout.write('\n📦 RELEVANT INSTALLED APPS')
        self.stdout.write('=' * 50)
        relevant_apps = ['storages', 'gallery', 'products']
        for app in relevant_apps:
            if app in settings.INSTALLED_APPS:
                self.stdout.write(f"✅ {app}")
            else:
                self.stdout.write(f"❌ {app} - NOT INSTALLED")
                
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('🎯 DIAGNOSIS COMPLETE'))
