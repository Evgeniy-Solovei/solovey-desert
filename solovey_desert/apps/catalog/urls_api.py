from django.urls import path

from . import api

app_name = 'catalog_api'

urlpatterns = [
    path('categories/', api.CategoryListAPIView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', api.CategoryDetailAPIView.as_view(), name='category_detail'),
    path('products/', api.ProductListAPIView.as_view(), name='product_list'),
    path('products/<slug:slug>/', api.ProductDetailAPIView.as_view(), name='product_detail'),
]
