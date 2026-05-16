from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('line_total',)


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ('key', 'session_key', 'total_quantity', 'total_price', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CartItemInline]


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('line_total',)


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('public_id', 'phone', 'status', 'total_price', 'event_date', 'created_at')
    list_filter = ('status', 'created_at', 'event_date')
    search_fields = ('public_id', 'phone', 'customer_name', 'email', 'comment')
    readonly_fields = ('public_id', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
# Register your models here.
