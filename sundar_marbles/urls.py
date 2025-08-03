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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),
]

# Only include other app URLs if they exist
try:
    from gallery.urls import urlpatterns as gallery_urls
    urlpatterns.append(path('api/gallery/', include('gallery.urls')))
except ImportError:
    pass

try:
    from contact.urls import urlpatterns as contact_urls
    urlpatterns.append(path('api/contact/', include('contact.urls')))
except ImportError:
    pass

# Only include debug views if they exist
try:
    from .debug_views import debug_database, force_create_superuser
    urlpatterns.extend([
        path('debug/database/', debug_database, name='debug_database'),
        path('debug/create-superuser/', force_create_superuser, name='force_create_superuser'),
    ])
except ImportError:
    pass

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

# Admin site customization
admin.site.site_header = "Sundar Marbles Administration"
admin.site.site_title = "Sundar Marbles Admin"
admin.site.index_title = "Welcome to Sundar Marbles Administration"
