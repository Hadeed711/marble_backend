from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryCategory, GalleryImage, GalleryTag, GalleryImageTag


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order', 'image_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order', 'name']

    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = "Images"


class GalleryImageTagInline(admin.TabularInline):
    model = GalleryImageTag
    extra = 1


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'project_location', 'is_active', 'is_featured', 'image_preview', 'created_at']
    list_filter = ['category', 'is_active', 'is_featured', 'completion_date', 'created_at']
    search_fields = ['title', 'description', 'project_location']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    inlines = [GalleryImageTagInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'image', 'image_preview', 'alt_text')
        }),
        ('Project Details', {
            'fields': ('project_location', 'completion_date')
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status & Display', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"


@admin.register(GalleryTag)
class GalleryTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'usage_count', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']

    def usage_count(self, obj):
        return obj.tagged_images.count()
    usage_count.short_description = "Usage Count"
