from rest_framework import serializers
from .models import GalleryCategory, GalleryImage, GalleryTag


class GalleryCategorySerializer(serializers.ModelSerializer):
    image_count = serializers.SerializerMethodField()

    class Meta:
        model = GalleryCategory
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'order', 'image_count']

    def get_image_count(self, obj):
        return obj.images.filter(is_active=True).count()


class GalleryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryTag
        fields = ['id', 'name', 'slug']


class GalleryImageSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImage
        fields = [
            'id', 'title', 'description', 'category', 'category_name',
            'image', 'alt_text', 'project_location', 'completion_date',
            'is_active', 'is_featured', 'order', 'tags', 'created_at'
        ]

    def get_tags(self, obj):
        tags = GalleryTag.objects.filter(tagged_images__image=obj)
        return GalleryTagSerializer(tags, many=True).data


class GalleryImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = [
            'title', 'description', 'category', 'image', 'alt_text',
            'project_location', 'completion_date', 'meta_title', 'meta_description',
            'is_active', 'is_featured', 'order'
        ]
