"""
Production settings for Azure deployment
This file will be used when DJANGO_SETTINGS_MODULE=sundar_marbles.settings_production
"""

import os
import dj_database_url
from decouple import config
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kTvi#=!ucz6tMDQpqK=W#t0y^y7yzXxLUCN5xc^uy3F^MzAv(N'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allow all hosts for Azure (you can restrict this later)
ALLOWED_HOSTS = [
    'sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net',
    'sundarmarbles.live',
    'www.sundarmarbles.live',
    'localhost',
    '127.0.0.1'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'storages',  # Required for Azure Blob Storage (products only)
    'gallery',
    'contact',
    'products',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sundar_marbles.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sundar_marbles.wsgi.application'

# Database configuration for production
DATABASES = {
    'default': dj_database_url.parse(config('DATABASE_URL'))
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Azure Blob Storage configuration for media files (FIXED WITH NEW STORAGES SYNTAX)
try:
    if not DEBUG and config('AZURE_ACCOUNT_NAME', default=None) and config('AZURE_ACCOUNT_KEY', default=None):
        # Production: Use Azure Blob Storage with NEW Django 4.2+ STORAGES syntax
        AZURE_ACCOUNT_NAME = config('AZURE_ACCOUNT_NAME')
        AZURE_ACCOUNT_KEY = config('AZURE_ACCOUNT_KEY')
        AZURE_CONTAINER = config('AZURE_CONTAINER', default='media')
        
        # ✅ USE NEW STORAGES CONFIGURATION (Django 4.2+)
        STORAGES = {
            "default": {
                "BACKEND": "storages.backends.azure_storage.AzureStorage",
            },
            "staticfiles": {
                "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
            },
        }
        
        # Azure Storage Settings
        AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
        MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/'
        
        # Additional Azure settings for proper operation
        AZURE_CONNECTION_TIMEOUT_SECS = 60
        AZURE_BLOB_MAX_MEMORY_SIZE = 2*1024*1024  # 2MB
        AZURE_OVERWRITE_FILES = True  # Allow overwriting existing files
        AZURE_LOCATION = ''  # Root of container
        
        print(f"[SUCCESS] Production: Using Azure Blob Storage with NEW STORAGES syntax: {MEDIA_URL}")
        
    elif config('AZURE_STORAGE_CONNECTION_STRING', default=None):
        # Alternative: Azure Blob Storage settings using connection string
        AZURE_STORAGE_CONNECTION_STRING = config('AZURE_STORAGE_CONNECTION_STRING')
        AZURE_CONTAINER = config('AZURE_CONTAINER', default='media')
        
        # Extract account name from connection string for media URL
        import re
        account_match = re.search(r'AccountName=([^;]+)', AZURE_STORAGE_CONNECTION_STRING)
        AZURE_ACCOUNT_NAME = account_match.group(1) if account_match else 'sundarmarbles'
        
        # ✅ USE NEW STORAGES CONFIGURATION (Django 4.2+)
        STORAGES = {
            "default": {
                "BACKEND": "storages.backends.azure_storage.AzureStorage",
            },
            "staticfiles": {
                "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
            },
        }
        
        AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
        MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/'
        
        # Additional Azure settings for proper operation
        AZURE_CONNECTION_TIMEOUT_SECS = 60
        AZURE_BLOB_MAX_MEMORY_SIZE = 2*1024*1024  # 2MB
        AZURE_OVERWRITE_FILES = True  # Allow overwriting existing files
        AZURE_LOCATION = ''  # Root of container
        
        print(f"[SUCCESS] Production: Using Azure Blob Storage (connection string) with NEW STORAGES syntax: {MEDIA_URL}")
    else:
        # Local media files (fallback)
        STORAGES = {
            "default": {
                "BACKEND": "django.core.files.storage.FileSystemStorage",
            },
            "staticfiles": {
                "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
            },
        }
        MEDIA_URL = '/media/'
        MEDIA_ROOT = BASE_DIR / 'media'
        print(f"[WARNING] Production: Using local media storage: {MEDIA_URL}")

except Exception as e:
    # Fallback to local storage if Azure configuration fails
    print(f"[WARNING] Azure storage configuration failed: {e}")
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    print(f"[FALLBACK] Falling back to local media storage: {MEDIA_URL}")

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 8  # Changed from 20 to 8 for better initial loading performance
}

# CORS settings
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS', 
    default='http://localhost:3000,http://127.0.0.1:3000,https://sundarmarbles.live',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

CORS_ALLOW_CREDENTIALS = True

# CSRF settings for Vercel routing
CSRF_TRUSTED_ORIGINS = [
    'https://sundarmarbles.live',
    'https://www.sundarmarbles.live',
    'https://sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net',
]

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'

# WhatsApp Configuration
WHATSAPP_NUMBER = config('WHATSAPP_NUMBER', default='923006641727')
WHATSAPP_API_URL = config('WHATSAPP_API_URL', default='https://api.whatsapp.com/send')

# Production security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'  # Changed from DENY to allow admin through domain routing

# Static files compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'