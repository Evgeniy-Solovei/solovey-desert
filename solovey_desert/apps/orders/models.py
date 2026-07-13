import uuid
from decimal import Decimal

from django.db import models

from apps.catalog.models import Product, ProductWeightOption


class Cart(models.Model):
    key = models.UUIDField('Постоянный ключ корзины', default=uuid.uuid4, unique=True, editable=False)
    session_key = models.CharField('Ключ сессии', max_length=40, unique=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['updated_at']),
        ]

    def __str__(self):
        return str(self.key)

    @property
    def total_price(self):
        return sum((item.line_total for item in self.items.select_related('product', 'weight_option')), Decimal('0'))

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name='Корзина', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    weight_option = models.ForeignKey(
        ProductWeightOption,
        verbose_name='Вариант веса',
        on_delete=models.PROTECT,
    )
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField('Цена на момент добавления', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Позиция корзины'
        verbose_name_plural = 'Позиции корзины'
        indexes = [
            models.Index(fields=['cart', 'updated_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'product', 'weight_option'],
                name='unique_cart_product_weight',
            ),
        ]

    def __str__(self):
        return f'{self.product} x {self.quantity}'

    @property
    def line_total(self):
        return self.price * self.quantity


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Новый'
        CONTACTED = 'contacted', 'Связались'
        CONFIRMED = 'confirmed', 'Подтвержден'
        CANCELLED = 'cancelled', 'Отменен'

    public_id = models.UUIDField('Публичный ID', default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField('Статус', max_length=20, choices=Status.choices, default=Status.NEW)
    customer_name = models.CharField('Имя', max_length=140, blank=True)
    phone = models.CharField('Телефон', max_length=40)
    email = models.EmailField('Email', blank=True)
    event_date = models.DateField('Дата события', null=True, blank=True)
    comment = models.TextField('Комментарий', blank=True)
    total_price = models.DecimalField('Итого', max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return f'Заказ {self.public_id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', null=True, blank=True, on_delete=models.SET_NULL)
    product_title = models.CharField('Название товара', max_length=180)
    weight = models.DecimalField('Вес', max_digits=7, decimal_places=2)
    weight_unit = models.CharField(
        'Единица',
        max_length=2,
        choices=ProductWeightOption.WeightUnit.choices,
        default=ProductWeightOption.WeightUnit.KG,
    )
    quantity = models.PositiveIntegerField('Количество')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    line_total = models.DecimalField('Сумма', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return self.product_title

# Create your models here.
