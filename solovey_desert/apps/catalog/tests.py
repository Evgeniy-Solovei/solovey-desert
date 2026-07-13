from django.test import TestCase

from apps.catalog.models import Category, Product, ProductWeightOption
from apps.catalog.utils import slugify_title, unique_slug_for_instance


class SlugGenerationTests(TestCase):
    def test_slugify_title_transliterates_cyrillic(self):
        self.assertEqual(slugify_title('Торт Клубника-ваниль'), 'tort-klubnika-vanil')

    def test_category_generates_slug_on_save(self):
        category = Category.objects.create(title='Десерты')
        self.assertEqual(category.slug, 'deserty')

    def test_product_generates_unique_slug(self):
        category = Category.objects.create(title='Категория', slug='category')
        Product.objects.create(category=category, title='Муссовое пирожное', slug='mousse-dessert')
        product = Product(category=category, title='Муссовое пирожное')
        product.slug = unique_slug_for_instance(product)
        self.assertEqual(product.slug, 'mousse-dessert-1')

    def test_category_regenerates_slug_when_title_changes(self):
        category = Category.objects.create(title='Десерты')
        category.title = 'Торты'
        category.save()
        self.assertEqual(category.slug, 'torty')

    def test_product_keeps_slug_when_title_unchanged(self):
        category = Category.objects.create(title='Категория', slug='category')
        product = Product.objects.create(category=category, title='Муссовое пирожное')
        original_slug = product.slug
        product.short_description = 'Обновлённое описание'
        product.save()
        self.assertEqual(product.slug, original_slug)


class WeightOptionTests(TestCase):
    def test_weight_label_for_kg(self):
        category = Category.objects.create(title='Торты')
        product = Product.objects.create(category=category, title='Торт')
        option = ProductWeightOption.objects.create(
            product=product,
            weight='1.50',
            weight_unit=ProductWeightOption.WeightUnit.KG,
            price=100,
        )
        self.assertEqual(option.weight_label, '1,5 кг')

    def test_weight_label_for_grams(self):
        category = Category.objects.create(title='Десерты')
        product = Product.objects.create(category=category, title='Пирожное')
        option = ProductWeightOption.objects.create(
            product=product,
            weight='120',
            weight_unit=ProductWeightOption.WeightUnit.G,
            price=15,
        )
        self.assertEqual(option.weight_label, '120 г')
