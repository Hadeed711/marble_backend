from django.core.management.base import BaseCommand
from django.conf import settings
import sys
import traceback


class Command(BaseCommand):
    help = 'Diagnose Django configuration issues causing 500 errors'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Diagnosing Django Configuration...'))
        
        errors = []
        warnings = []
        
        # Test 1: Check Django settings
        self.stdout.write('\n📋 Test 1: Checking Django settings...')
        try:
            self.stdout.write(f"DEBUG: {settings.DEBUG}")
            self.stdout.write(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
            self.stdout.write(f"SECRET_KEY: {'✅ Set' if settings.SECRET_KEY else '❌ Missing'}")
            self.stdout.write(f"INSTALLED_APPS: {len(settings.INSTALLED_APPS)} apps")
        except Exception as e:
            errors.append(f"Settings error: {e}")
        
        # Test 2: Check database connection
        self.stdout.write('\n🗃️  Test 2: Testing database connection...')
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write(self.style.SUCCESS("✅ Database connection working"))
        except Exception as e:
            errors.append(f"Database error: {e}")
            self.stdout.write(self.style.ERROR(f"❌ Database error: {e}"))
        
        # Test 3: Check storage configuration
        self.stdout.write('\n☁️  Test 3: Checking storage configuration...')
        try:
            from django.core.files.storage import default_storage
            storage_class = default_storage.__class__.__name__
            self.stdout.write(f"Storage backend: {storage_class}")
            
            if hasattr(settings, 'STORAGES'):
                self.stdout.write("✅ STORAGES configuration found")
                default_backend = settings.STORAGES.get('default', {}).get('BACKEND', 'Not set')
                self.stdout.write(f"Default storage: {default_backend}")
            else:
                warnings.append("STORAGES configuration missing")
                
        except Exception as e:
            errors.append(f"Storage configuration error: {e}")
        
        # Test 4: Check environment variables
        self.stdout.write('\n🌐 Test 4: Checking environment variables...')
        try:
            from decouple import config
            required_vars = [
                'SECRET_KEY',
                'DATABASE_URL',
                'AZURE_ACCOUNT_NAME',
                'AZURE_ACCOUNT_KEY'
            ]
            
            for var in required_vars:
                value = config(var, default=None)
                status = "✅" if value else "❌"
                self.stdout.write(f"{status} {var}: {'Set' if value else 'Missing'}")
                if not value:
                    errors.append(f"Missing environment variable: {var}")
                    
        except Exception as e:
            errors.append(f"Environment variables error: {e}")
        
        # Test 5: Check imports
        self.stdout.write('\n📦 Test 5: Testing critical imports...')
        critical_imports = [
            'django.contrib.admin',
            'rest_framework',
            'corsheaders',
            'storages',
            'products'
        ]
        
        for module_name in critical_imports:
            try:
                __import__(module_name)
                self.stdout.write(f"✅ {module_name}")
            except ImportError as e:
                errors.append(f"Import error for {module_name}: {e}")
                self.stdout.write(f"❌ {module_name}: {e}")
        
        # Test 6: Check URL configuration
        self.stdout.write('\n🔗 Test 6: Testing URL configuration...')
        try:
            from django.urls import reverse
            admin_url = reverse('admin:index')
            self.stdout.write(f"✅ Admin URL: {admin_url}")
        except Exception as e:
            errors.append(f"URL configuration error: {e}")
            self.stdout.write(f"❌ URL error: {e}")
        
        # Test 7: Check static files
        self.stdout.write('\n📁 Test 7: Checking static files configuration...')
        try:
            self.stdout.write(f"STATIC_URL: {settings.STATIC_URL}")
            self.stdout.write(f"STATIC_ROOT: {settings.STATIC_ROOT}")
            if hasattr(settings, 'STATICFILES_DIRS'):
                self.stdout.write(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        except Exception as e:
            errors.append(f"Static files error: {e}")
        
        # Summary
        self.stdout.write('\n' + '='*50)
        if errors:
            self.stdout.write(self.style.ERROR(f'❌ FOUND {len(errors)} CRITICAL ERRORS:'))
            for i, error in enumerate(errors, 1):
                self.stdout.write(self.style.ERROR(f'   {i}. {error}'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ No critical errors found'))
            
        if warnings:
            self.stdout.write(self.style.WARNING(f'\n⚠️  FOUND {len(warnings)} WARNINGS:'))
            for i, warning in enumerate(warnings, 1):
                self.stdout.write(self.style.WARNING(f'   {i}. {warning}'))
        
        # Recommendations
        self.stdout.write(self.style.SUCCESS('\n💡 RECOMMENDATIONS:'))
        
        if errors:
            self.stdout.write('1. Fix the critical errors listed above')
            self.stdout.write('2. Check Azure App Service logs for detailed error messages')
            self.stdout.write('3. Verify all environment variables are set in Azure')
            self.stdout.write('4. Ensure all required packages are installed')
        else:
            self.stdout.write('1. Check Azure App Service application logs')
            self.stdout.write('2. Restart the Azure App Service')
            self.stdout.write('3. Verify the deployment completed successfully')
        
        self.stdout.write('\n🔗 Check Azure logs at:')
        self.stdout.write('   https://portal.azure.com -> App Service -> Monitoring -> Log stream')
        
        return errors
