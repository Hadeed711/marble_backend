"""
WSGI config for sundar_marbles project - Azure Production Version

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Add project directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# NUCLEAR FIX: Force production settings - override everything
os.environ['DJANGO_SETTINGS_MODULE'] = 'sundar_marbles.settings_production'

# Force environment variables for Azure
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('SECRET_KEY', 'kTvi#=!ucz6tMDQpqK=W#t0y^y7yzXxLUCN5xc^uy3F^MzAv(N')
os.environ.setdefault('ALLOWED_HOSTS', 'sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net,localhost,127.0.0.1')

# Import and configure Django
import django
from django.conf import settings

# Ensure settings are loaded
django.setup()

# Create WSGI application
application = get_wsgi_application()
