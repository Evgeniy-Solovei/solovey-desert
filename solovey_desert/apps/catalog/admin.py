from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Category, Product, ProductImage, ProductWeightOption


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'is_featured', 'order')
    list_editable = ('is_active', 'is_featured', 'order')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1


class ProductWeightOptionInline(TabularInline):
    model = ProductWeightOption
    extra = 1
    fields = ('weight', 'weight_unit', 'price', 'is_default', 'order')


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('title', 'category', 'price_from', 'is_active', 'is_featured', 'order')
    list_editable = ('price_from', 'is_active', 'is_featured', 'order')
    list_filter = ('category', 'is_active', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description', 'description')
    inlines = [ProductWeightOptionInline, ProductImageInline]
# Register your models here.
