from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Setup production environment - run migrations and create superuser'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up production environment...'))
        
        # Run migrations
        self.stdout.write('Running migrations...')
        from django.core.management import call_command
        call_command('migrate')
        
        # Collect static files
        self.stdout.write('Collecting static files...')
        call_command('collectstatic', '--noinput')
        
        # Create superuser if it doesn't exist
        self.stdout.write('Creating superuser...')
        try:
            with transaction.atomic():
                if not User.objects.filter(username='admin').exists():
                    User.objects.create_superuser(
                        username='admin',
                        email='admin@sundarmarbles.com',
                        password='sundar123'  # Change this after first login
                    )
                    self.stdout.write(
                        self.style.SUCCESS('Superuser created: admin/sundar123')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('Superuser already exists')
                    )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Production setup completed successfully!')
        )
