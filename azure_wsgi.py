"""
Azure-specific WSGI configuration for sundar_marbles project.
This file is specifically designed for Azure App Service deployment.
"""

import os
import sys
from pathlib import Path

# Add project directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# FORCE production settings for Azure
os.environ['DJANGO_SETTINGS_MODULE'] = 'sundar_marbles.settings_production'

# Force critical environment variables
os.environ['DEBUG'] = 'False'
os.environ['SECRET_KEY'] = 'kTvi#=!ucz6tMDQpqK=W#t0y^y7yzXxLUCN5xc^uy3F^MzAv(N'
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_qrXsNK3Jpk8i@ep-divine-tooth-a8gxgnc6-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require'
os.environ['ALLOWED_HOSTS'] = 'sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net,localhost,127.0.0.1,sundarmarbles.live,www.sundarmarbles.live'

# Test database connection before starting
try:
    import django
    from django.conf import settings
    django.setup()
    
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
        print("✅ Database connection successful in WSGI")
except Exception as e:
    print(f"❌ Database connection failed in WSGI: {e}")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
