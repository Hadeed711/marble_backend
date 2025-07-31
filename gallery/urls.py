from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('categories/', views.GalleryCategoryListView.as_view(), name='category-list'),
    path('categories/with-count/', views.gallery_categories_with_count, name='categories-with-count'),
    path('images/', views.GalleryImageListView.as_view(), name='image-list'),
    path('images/featured/', views.FeaturedGalleryImagesView.as_view(), name='featured-images'),
    path('images/<int:id>/', views.GalleryImageDetailView.as_view(), name='image-detail'),
]
