from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('catalog/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
