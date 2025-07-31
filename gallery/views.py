from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from .models import GalleryCategory, GalleryImage
from .serializers import GalleryCategorySerializer, GalleryImageSerializer


class GalleryCategoryListView(generics.ListAPIView):
    queryset = GalleryCategory.objects.filter(is_active=True).order_by('order', 'name')
    serializer_class = GalleryCategorySerializer


class GalleryImageListView(generics.ListAPIView):
    queryset = GalleryImage.objects.filter(is_active=True)
    serializer_class = GalleryImageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['title', 'description', 'project_location']
    ordering_fields = ['title', 'completion_date', 'created_at', 'order']
    ordering = ['category', 'order', '-created_at']


class GalleryImageDetailView(generics.RetrieveAPIView):
    queryset = GalleryImage.objects.filter(is_active=True)
    serializer_class = GalleryImageSerializer
    lookup_field = 'id'


class FeaturedGalleryImagesView(generics.ListAPIView):
    queryset = GalleryImage.objects.filter(is_active=True, is_featured=True)
    serializer_class = GalleryImageSerializer


@api_view(['GET'])
def gallery_categories_with_count(request):
    """Get all gallery categories with image count"""
    categories = GalleryCategory.objects.filter(is_active=True).order_by('order', 'name')
    data = []
    for category in categories:
        data.append({
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'image_count': category.images.filter(is_active=True).count()
        })
    return Response(data)
