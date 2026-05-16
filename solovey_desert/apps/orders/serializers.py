from django.db import transaction
from django.conf import settings
from rest_framework import serializers

from apps.catalog.models import Product, ProductWeightOption
from apps.catalog.serializers import ProductListSerializer, ProductWeightOptionSerializer

from .models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    weight_option = ProductWeightOptionSerializer(read_only=True)
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'weight_option', 'quantity', 'price', 'line_total')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_price', 'total_quantity', 'updated_at')


class CartItemCreateSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True),
        source='product',
    )
    weight_option_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductWeightOption.objects.select_related('product'),
        source='weight_option',
    )
    quantity = serializers.IntegerField(min_value=1, max_value=settings.CART_MAX_ITEM_QUANTITY, default=1)

    def validate(self, attrs):
        product = attrs['product']
        weight_option = attrs['weight_option']
        if weight_option.product_id != product.id:
            raise serializers.ValidationError('Вариант веса не относится к выбранному товару.')
        if not weight_option.product.is_active:
            raise serializers.ValidationError('Товар недоступен для заказа.')
        return attrs

    def create(self, validated_data):
        cart = self.context['cart']
        product = validated_data['product']
        weight_option = validated_data['weight_option']
        quantity = validated_data['quantity']
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            weight_option=weight_option,
            defaults={'quantity': quantity, 'price': weight_option.price},
        )
        if not created:
            item.quantity = min(item.quantity + quantity, settings.CART_MAX_ITEM_QUANTITY)
            item.save(update_fields=['quantity', 'updated_at'])
        return item


class CartItemUpdateSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, max_value=settings.CART_MAX_ITEM_QUANTITY)

    class Meta:
        model = CartItem
        fields = ('quantity',)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product_title', 'weight', 'quantity', 'price', 'line_total')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'public_id',
            'status',
            'customer_name',
            'phone',
            'email',
            'event_date',
            'comment',
            'total_price',
            'items',
            'created_at',
        )
        read_only_fields = ('public_id', 'status', 'total_price', 'items', 'created_at')


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('customer_name', 'phone', 'email', 'event_date', 'comment')

    def validate(self, attrs):
        cart = self.context['cart']
        if not cart.items.exists():
            raise serializers.ValidationError('Корзина пустая.')
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        cart = self.context['cart']
        cart_items = cart.items.select_related('product', 'weight_option')
        order = Order.objects.create(total_price=cart.total_price, **validated_data)
        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=item.product,
                    product_title=item.product.title,
                    weight=item.weight_option.weight,
                    quantity=item.quantity,
                    price=item.price,
                    line_total=item.line_total,
                )
                for item in cart_items
            ]
        )
        cart.items.all().delete()
        return order
