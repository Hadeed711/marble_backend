from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'order']
    
    def get_readonly_fields(self, request, obj=None):
        # Make image preview read-only to avoid issues
        return self.readonly_fields


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_active', 'is_featured', 'image_preview', 'created_at']
    list_filter = ['category', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'description', 'meta_title']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category', 'image', 'image_preview')
        }),
        ('Pricing & Specifications', {
            'fields': ('price', 'origin', 'finish', 'thickness')
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            try:
                return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
            except Exception as e:
                return f"Image error: {str(e)}"
        return "No Image"
    image_preview.short_description = "Image Preview"
    
    def save_model(self, request, obj, form, change):
        try:
            # Ensure category exists
            if not obj.category:
                raise ValidationError("Category is required")
            
            # Validate image if present
            if obj.image:
                # Check file size (limit to 5MB)
                if obj.image.size > 5 * 1024 * 1024:
                    messages.error(request, "Image file too large. Maximum size is 5MB.")
                    return
                
                # Check file extension
                allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp']
                file_extension = obj.image.name.lower().split('.')[-1]
                if f'.{file_extension}' not in allowed_extensions:
                    messages.error(request, f"Invalid file type. Allowed: {', '.join(allowed_extensions)}")
                    return
            
            super().save_model(request, obj, form, change)
            
            if change:
                messages.success(request, f"Product '{obj.name}' updated successfully!")
            else:
                messages.success(request, f"Product '{obj.name}' created successfully!")
                
        except Exception as e:
            messages.error(request, f"Error saving product: {str(e)}")
            # Re-raise the exception to prevent saving with errors
            raise


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text', 'is_primary', 'order', 'image_preview', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name', 'alt_text']
    readonly_fields = ['created_at', 'image_preview']

    def image_preview(self, obj):
        if obj.image:
            try:
                return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
            except Exception as e:
                return f"Image error: {str(e)}"
        return "No Image"
    image_preview.short_description = "Image Preview"
    
    def save_model(self, request, obj, form, change):
        try:
            # Validate image if present
            if obj.image:
                # Check file size (limit to 5MB)
                if obj.image.size > 5 * 1024 * 1024:
                    messages.error(request, "Image file too large. Maximum size is 5MB.")
                    return
                
                # Check file extension
                allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp']
                file_extension = obj.image.name.lower().split('.')[-1]
                if f'.{file_extension}' not in allowed_extensions:
                    messages.error(request, f"Invalid file type. Allowed: {', '.join(allowed_extensions)}")
                    return
            
            super().save_model(request, obj, form, change)
            messages.success(request, f"Product image for '{obj.product.name}' saved successfully!")
                
        except Exception as e:
            messages.error(request, f"Error saving product image: {str(e)}")
            raise
