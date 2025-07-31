from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/with-count/', views.product_categories_with_count, name='categories-with-count'),
    path('', views.ProductListView.as_view(), name='product-list'),
    path('featured/', views.FeaturedProductsView.as_view(), name='featured-products'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
]
