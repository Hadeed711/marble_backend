"""
Temporary debug settings for troubleshooting Azure deployment issues.
This file should only be used temporarily to debug the admin login issue.
"""

from .settings_production import *

# Temporarily enable debug for troubleshooting
DEBUG = True

# Add more detailed logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.contrib.auth': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.contrib.sessions': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# More permissive CORS for debugging
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Session settings
SESSION_COOKIE_SECURE = False  # Temporarily disable for debugging
CSRF_COOKIE_SECURE = False    # Temporarily disable for debugging
SESSION_COOKIE_AGE = 3600     # 1 hour
