"""
Management command to set up production database
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Set up production database with migrations and superuser'

    def handle(self, *args, **options):
        self.stdout.write('Starting production database setup...')
        
        # Test database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                self.stdout.write(self.style.SUCCESS('✅ Database connection successful'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Database connection failed: {e}'))
            return
        
        # Run migrations
        try:
            self.stdout.write('Running migrations...')
            call_command('migrate', verbosity=2)
            self.stdout.write(self.style.SUCCESS('✅ Migrations completed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Migration failed: {e}'))
            return
        
        # Create superuser
        try:
            User = get_user_model()
            
            # Delete existing admin if exists
            if User.objects.filter(username='admin').exists():
                User.objects.filter(username='admin').delete()
                self.stdout.write('Deleted existing admin user')
            
            # Create new superuser
            user = User.objects.create_superuser(
                username='admin',
                email='admin@sundarmarbles.com', 
                password='admin123456'
            )
            self.stdout.write(self.style.SUCCESS('✅ Superuser created: admin / admin123456'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Failed to create superuser: {e}'))
        
        # Collect static files
        try:
            self.stdout.write('Collecting static files...')
            call_command('collectstatic', interactive=False, clear=True)
            self.stdout.write(self.style.SUCCESS('✅ Static files collected'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Static files collection failed: {e}'))
        
        self.stdout.write(self.style.SUCCESS('Production setup completed!'))
