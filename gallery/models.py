from django.db import models
from django.utils.text import slugify


class GalleryCategory(models.Model):
    """Categories for gallery images like Stairs, Floors, Mosaic, etc."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Gallery Category"
        verbose_name_plural = "Gallery Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """Gallery images for showcasing work"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/', help_text="Gallery image")
    alt_text = models.CharField(max_length=200, blank=True)
    
    # Project details
    project_location = models.CharField(max_length=200, blank=True, help_text="Location of the project")
    completion_date = models.DateField(blank=True, null=True)
    
    # SEO and metadata
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=500, blank=True)
    
    # Status and visibility
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, help_text="Display order within category")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        ordering = ['category', 'order', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.category.name}"


class GalleryTag(models.Model):
    """Tags for gallery images"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Gallery Tag"
        verbose_name_plural = "Gallery Tags"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Many-to-many relationship between GalleryImage and GalleryTag
class GalleryImageTag(models.Model):
    """Junction table for gallery images and tags"""
    image = models.ForeignKey(GalleryImage, on_delete=models.CASCADE, related_name='image_tags')
    tag = models.ForeignKey(GalleryTag, on_delete=models.CASCADE, related_name='tagged_images')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('image', 'tag')
        verbose_name = "Gallery Image Tag"
        verbose_name_plural = "Gallery Image Tags"

    def __str__(self):
        return f"{self.image.title} - {self.tag.name}"
