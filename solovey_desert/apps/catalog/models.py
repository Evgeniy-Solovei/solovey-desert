from django.db import models
from django.urls import reverse

from .utils import ensure_slug_for_instance


class Category(models.Model):
    title = models.CharField('Название', max_length=160)
    slug = models.SlugField('Slug', max_length=180, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to='categories/', blank=True)
    is_active = models.BooleanField('Активна', default=True)
    is_featured = models.BooleanField('На главной', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        indexes = [
            models.Index(fields=['is_active', 'order']),
            models.Index(fields=['is_featured', 'order']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:category_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        ensure_slug_for_instance(self)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='products',
        on_delete=models.PROTECT,
    )
    title = models.CharField('Название', max_length=180)
    slug = models.SlugField('Slug', max_length=200, unique=True, blank=True)
    short_description = models.CharField('Краткое описание', max_length=260, blank=True)
    description = models.TextField('Описание', blank=True)
    taste_description = models.TextField('Описание вкуса', blank=True)
    composition = models.TextField('Состав', blank=True)
    note = models.CharField('Примечание', max_length=300, blank=True)
    main_image = models.ImageField('Главное изображение', upload_to='products/', blank=True)
    price_from = models.DecimalField('Цена от', max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField('Активен', default=True)
    is_featured = models.BooleanField('Популярный', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [
            models.Index(fields=['is_active', 'order']),
            models.Index(fields=['is_featured', 'order']),
            models.Index(fields=['category', 'is_active', 'order']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        ensure_slug_for_instance(self)
        super().save(*args, **kwargs)

    @property
    def default_weight_option(self):
        prefetched = getattr(self, '_prefetched_objects_cache', {}).get('weight_options')
        options = list(prefetched) if prefetched is not None else list(self.weight_options.all())
        return next((option for option in options if option.is_default), None) or (options[0] if options else None)


class ProductWeightOption(models.Model):
    class WeightUnit(models.TextChoices):
        KG = 'kg', 'кг'
        G = 'g', 'г'
        PCS = 'pc', 'шт'

    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        related_name='weight_options',
        on_delete=models.CASCADE,
    )
    weight = models.DecimalField('Значение', max_digits=7, decimal_places=2)
    weight_unit = models.CharField(
        'Единица',
        max_length=2,
        choices=WeightUnit.choices,
        default=WeightUnit.KG,
    )
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    is_default = models.BooleanField('По умолчанию', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'weight']
        verbose_name = 'Вариант'
        verbose_name_plural = 'Варианты'
        indexes = [
            models.Index(fields=['product', 'order']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'weight', 'weight_unit'],
                name='unique_product_weight',
            ),
        ]

    def __str__(self):
        return f'{self.product} - {self.weight_label}'

    @property
    def weight_label(self):
        unit_label = dict(self.WeightUnit.choices).get(self.weight_unit, 'кг')
        if self.weight == self.weight.to_integral_value():
            value = int(self.weight)
        else:
            value = f'{self.weight:g}'.replace('.', ',')
        return f'{value} {unit_label}'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = models.ImageField('Изображение', upload_to='products/gallery/')
    alt = models.CharField('Alt', max_length=180, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товара'
        indexes = [
            models.Index(fields=['product', 'order']),
        ]

    def __str__(self):
        return self.alt or str(self.product)

# Create your models here.
