"""
WSGI config for sundar_marbles project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# FORCE production settings - bypass all environment variable issues
os.environ['DJANGO_SETTINGS_MODULE'] = 'sundar_marbles.settings_production'

application = get_wsgi_application()
