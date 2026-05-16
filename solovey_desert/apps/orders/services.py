import uuid

from django.conf import settings
from django.db.models import Prefetch

from apps.catalog.models import ProductWeightOption

from .models import Cart, CartItem


def cart_queryset():
    return Cart.objects.prefetch_related(
        Prefetch(
            'items',
            queryset=CartItem.objects.select_related('product', 'product__category', 'weight_option').prefetch_related(
                Prefetch(
                    'product__weight_options',
                    queryset=ProductWeightOption.objects.order_by('order', 'weight'),
                )
            ),
        )
    )


def get_or_create_cart(request):
    cookie_key = request.COOKIES.get(settings.CART_COOKIE_NAME)
    if cookie_key:
        try:
            cart_key = uuid.UUID(cookie_key)
        except ValueError:
            cart_key = None
        if cart_key:
            cart = cart_queryset().filter(key=cart_key).first()
            if cart:
                return cart

    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart_queryset().get(pk=cart.pk)


def attach_cart_cookie(response, cart):
    response.set_cookie(
        settings.CART_COOKIE_NAME,
        str(cart.key),
        max_age=settings.CART_COOKIE_AGE,
        secure=settings.CART_COOKIE_SECURE,
        httponly=True,
        samesite='Lax',
    )
    return response
