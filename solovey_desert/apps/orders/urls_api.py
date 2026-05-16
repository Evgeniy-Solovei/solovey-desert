from django.urls import path

from . import api

app_name = 'orders_api'

urlpatterns = [
    path('cart/', api.CartAPIView.as_view(), name='cart_detail'),
    path('cart/items/', api.CartItemCreateAPIView.as_view(), name='cart_item_create'),
    path('cart/items/<int:pk>/', api.CartItemDetailAPIView.as_view(), name='cart_item_detail'),
    path('orders/', api.OrderCreateAPIView.as_view(), name='order_create'),
    path('orders/<uuid:public_id>/', api.OrderDetailAPIView.as_view(), name='order_detail'),
]
