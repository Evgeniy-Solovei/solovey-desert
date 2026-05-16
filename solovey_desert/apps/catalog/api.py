from rest_framework import generics

from .models import Category, Product
from .serializers import CategorySerializer, ProductDetailSerializer, ProductListSerializer


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(is_active=True).order_by('order', 'title')


class CategoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Category.objects.filter(is_active=True).prefetch_related('products__weight_options')


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = (
            Product.objects.filter(is_active=True)
            .select_related('category')
            .prefetch_related('weight_options')
            .order_by('order', 'title')
        )
        category_slug = self.request.query_params.get('category')
        is_featured = self.request.query_params.get('is_featured')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug, category__is_active=True)

        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured.lower() in ('1', 'true', 'yes'))

        return queryset


class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True)
            .select_related('category')
            .prefetch_related('images', 'weight_options')
        )
