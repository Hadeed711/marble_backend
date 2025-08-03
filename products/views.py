from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductCreateSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class FeaturedProductsView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True, is_featured=True)
    serializer_class = ProductSerializer


@api_view(['GET'])
def product_categories_with_count(request):
    """Get all categories with product count"""
    categories = Category.objects.filter(is_active=True)
    data = []
    for category in categories:
        data.append({
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'product_count': category.products.filter(is_active=True).count()
        })
    return Response(data)


@api_view(['GET'])
def debug_storage(request):
    """Debug endpoint to check storage configuration"""
    try:
        debug_info = {
            'storage_backend': default_storage.__class__.__name__,
            'media_url': settings.MEDIA_URL,
            'azure_configured': hasattr(settings, 'AZURE_ACCOUNT_NAME'),
            'storages_config': getattr(settings, 'STORAGES', {}),
        }
        
        if hasattr(settings, 'AZURE_ACCOUNT_NAME'):
            debug_info.update({
                'azure_account': settings.AZURE_ACCOUNT_NAME,
                'azure_container': getattr(settings, 'AZURE_CONTAINER', 'Not set'),
                'azure_domain': getattr(settings, 'AZURE_CUSTOM_DOMAIN', 'Not set'),
            })
        
        return JsonResponse({
            'status': 'success',
            'debug_info': debug_info
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        })
