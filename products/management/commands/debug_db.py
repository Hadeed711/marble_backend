"""
Management command to test database connection and setup
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from django.core.management import call_command
import traceback


class Command(BaseCommand):
    help = 'Test database connection and force setup everything'

    def handle(self, *args, **options):
        self.stdout.write('=== COMPREHENSIVE DATABASE DEBUG ===')
        
        # 1. Test basic database connection
        self.stdout.write('\n1. Testing database connection...')
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT version()')
                version = cursor.fetchone()[0]
                self.stdout.write(self.style.SUCCESS(f'✅ Connected to: {version}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Database connection failed: {e}'))
            self.stdout.write(self.style.ERROR(f'Full error: {traceback.format_exc()}'))
            return
        
        # 2. Check if Django tables exist
        self.stdout.write('\n2. Checking Django tables...')
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name LIKE 'django_%' OR table_name LIKE 'auth_%'
                """)
                tables = cursor.fetchall()
                if tables:
                    self.stdout.write(self.style.SUCCESS(f'✅ Found Django tables: {[t[0] for t in tables]}'))
                else:
                    self.stdout.write(self.style.WARNING('⚠️ No Django tables found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Table check failed: {e}'))
        
        # 3. Force migrations
        self.stdout.write('\n3. Running migrations...')
        try:
            call_command('migrate', verbosity=2, interactive=False)
            self.stdout.write(self.style.SUCCESS('✅ Migrations completed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Migration failed: {e}'))
            self.stdout.write(self.style.ERROR(f'Full error: {traceback.format_exc()}'))
        
        # 4. Force create superuser
        self.stdout.write('\n4. Creating superuser...')
        try:
            User = get_user_model()
            
            # Delete all admin users
            deleted = User.objects.filter(username='admin').delete()
            if deleted[0] > 0:
                self.stdout.write(f'Deleted {deleted[0]} existing admin users')
            
            # Create new superuser
            user = User.objects.create_superuser(
                username='admin',
                email='admin@sundarmarbles.com',
                password='admin123456'
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Superuser created: {user.username} (ID: {user.id})'))
            
            # Verify superuser
            admin_user = User.objects.get(username='admin')
            self.stdout.write(f'Verification - Username: {admin_user.username}, Email: {admin_user.email}')
            self.stdout.write(f'Is superuser: {admin_user.is_superuser}, Is staff: {admin_user.is_staff}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Superuser creation failed: {e}'))
            self.stdout.write(self.style.ERROR(f'Full error: {traceback.format_exc()}'))
        
        # 5. Test authentication
        self.stdout.write('\n5. Testing authentication...')
        try:
            from django.contrib.auth import authenticate
            user = authenticate(username='admin', password='admin123456')
            if user:
                self.stdout.write(self.style.SUCCESS(f'✅ Authentication successful for {user.username}'))
            else:
                self.stdout.write(self.style.ERROR('❌ Authentication failed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Authentication test failed: {e}'))
        
        # 6. List all users
        self.stdout.write('\n6. Listing all users...')
        try:
            User = get_user_model()
            users = User.objects.all()
            for user in users:
                self.stdout.write(f'User: {user.username}, Email: {user.email}, Superuser: {user.is_superuser}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ User listing failed: {e}'))
        
        self.stdout.write('\n=== DEBUG COMPLETED ===')
        self.stdout.write(self.style.SUCCESS('Try logging in with: admin / admin123456'))
