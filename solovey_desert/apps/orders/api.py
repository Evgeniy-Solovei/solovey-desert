from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartItem, Order
from .serializers import (
    CartItemCreateSerializer,
    CartItemSerializer,
    CartItemUpdateSerializer,
    CartSerializer,
    OrderCreateSerializer,
    OrderSerializer,
)
from .services import attach_cart_cookie, get_or_create_cart


class CartAPIView(APIView):
    def get(self, request):
        cart = get_or_create_cart(request)
        serializer = CartSerializer(cart, context={'request': request})
        return attach_cart_cookie(Response(serializer.data), cart)


class CartItemCreateAPIView(APIView):
    def post(self, request):
        cart = get_or_create_cart(request)
        serializer = CartItemCreateSerializer(data=request.data, context={'cart': cart})
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        response_serializer = CartItemSerializer(item, context={'request': request})
        return attach_cart_cookie(Response(response_serializer.data, status=status.HTTP_201_CREATED), cart)


class CartItemDetailAPIView(APIView):
    def get_object(self, request, pk):
        cart = get_or_create_cart(request)
        return generics.get_object_or_404(CartItem, pk=pk, cart=cart)

    def patch(self, request, pk):
        item = self.get_object(request, pk)
        serializer = CartItemUpdateSerializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return attach_cart_cookie(Response(CartItemSerializer(item, context={'request': request}).data), item.cart)

    def delete(self, request, pk):
        item = self.get_object(request, pk)
        cart = item.cart
        item.delete()
        return attach_cart_cookie(Response(status=status.HTTP_204_NO_CONTENT), cart)


class OrderCreateAPIView(APIView):
    def post(self, request):
        cart = get_or_create_cart(request)
        serializer = OrderCreateSerializer(data=request.data, context={'cart': cart})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        response = Response(
            OrderSerializer(order, context={'request': request}).data, status=status.HTTP_201_CREATED
        )
        return attach_cart_cookie(response, cart)


class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    lookup_field = 'public_id'
    queryset = Order.objects.prefetch_related('items')
