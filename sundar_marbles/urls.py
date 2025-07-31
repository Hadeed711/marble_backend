"""
URL configuration for sundar_marbles project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .debug_views import debug_database, force_create_superuser
from .test_views import test_basic, test_database, test_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),
    path('api/gallery/', include('gallery.urls')),
    path('api/contact/', include('contact.urls')),
    
    # Debug endpoints for troubleshooting
    path('debug/database/', debug_database, name='debug_database'),
    path('debug/create-superuser/', force_create_superuser, name='force_create_superuser'),
    
    # Test endpoints
    path('test/basic/', test_basic, name='test_basic'),
    path('test/database/', test_database, name='test_database'),
    path('test/login/', test_login, name='test_login'),
]

# Serve media files in development and production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # In production, serve media files through Django (Azure doesn't support static file serving by default)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin site customization
admin.site.site_header = "Sundar Marbles Administration"
admin.site.site_title = "Sundar Marbles Admin"
admin.site.index_title = "Welcome to Sundar Marbles Administration"
