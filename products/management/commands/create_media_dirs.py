"""
Django management command to create media directories and test media serving
"""

from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Create media directories for products and gallery'

    def handle(self, *args, **options):
        self.stdout.write('Creating media directories...')
        
        # Create media directories
        media_dirs = [
            'products',
            'gallery',
        ]
        
        for directory in media_dirs:
            dir_path = os.path.join(settings.MEDIA_ROOT, directory)
            os.makedirs(dir_path, exist_ok=True)
            self.stdout.write(f'Created directory: {dir_path}')
        
        # Create .gitkeep files to ensure directories are tracked in git
        for directory in media_dirs:
            gitkeep_path = os.path.join(settings.MEDIA_ROOT, directory, '.gitkeep')
            with open(gitkeep_path, 'w') as f:
                f.write('')
            self.stdout.write(f'Created .gitkeep: {gitkeep_path}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created media directories!')
        )
