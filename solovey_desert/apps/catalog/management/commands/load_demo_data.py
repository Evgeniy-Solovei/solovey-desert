from decimal import Decimal

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from apps.catalog.models import Category, Product, ProductImage, ProductWeightOption
from apps.pages.models import HeroSlide


class Command(BaseCommand):
    help = 'Loads demo catalog content from the mockup assets.'

    def handle(self, *args, **options):
        categories = [
            ('Торты', 'cakes', 'Авторские торты для праздников, свадеб и семейных событий.', 'cake.jpg'),
            ('Десерты', 'desserts', 'Капкейки, муссовые пирожные, эклеры и сезонные позиции.', 'desserts.jpg'),
            ('Конфеты', 'candies', 'Корпусные конфеты и шоколадные наборы ручной работы.', 'candies.jpg'),
            ('Наборы', 'sets', 'Подарочные боксы под повод, дату и нужную цветовую гамму.', 'sets.jpg'),
        ]
        category_map = {}
        for index, (title, slug, description, image) in enumerate(categories):
            category, _ = Category.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'description': description,
                    'is_active': True,
                    'is_featured': True,
                    'order': index,
                },
            )
            self.attach_image(category, 'image', image, image)
            category_map[slug] = category

        products = [
            (
                'Торт Клубника-ваниль',
                'strawberry-vanilla-cake',
                'cakes',
                'Нежный бисквит, сливочный крем и ягодная начинка.',
                'product-cake.jpg',
                Decimal('120'),
                True,
            ),
            (
                'Торт Фисташка-малина',
                'pistachio-raspberry-cake',
                'cakes',
                'Фисташковый бисквит, малиновая кислинка и хруст белого шоколада.',
                'product-cake.jpg',
                Decimal('120'),
                True,
            ),
            (
                'Муссовое пирожное',
                'mousse-dessert',
                'desserts',
                'Воздушный мусс, хрустящий слой и мягкий декор.',
                'product-dessert.jpg',
                Decimal('85'),
                True,
            ),
            (
                'Конфеты ассорти',
                'assorted-candies',
                'candies',
                'Набор шоколадных конфет с разными начинками.',
                'product-candy.jpg',
                Decimal('55'),
                True,
            ),
            (
                'Подарочный набор',
                'gift-set',
                'sets',
                'Готовая коробка сладостей для красивого подарка.',
                'sets.jpg',
                Decimal('65'),
                True,
            ),
        ]
        for index, (title, slug, category_slug, short, image, price, featured) in enumerate(products):
            product, _ = Product.objects.update_or_create(
                slug=slug,
                defaults={
                    'category': category_map[category_slug],
                    'title': title,
                    'short_description': short,
                    'description': short,
                    'taste_description': 'Мягкая текстура, сбалансированная сладость и аккуратный декор под событие.',
                    'composition': 'Натуральные сливки, свежие яйца, сахар, пшеничная мука, ягодное пюре, шоколад.',
                    'note': '*Окончательная стоимость рассчитывается исходя из веса и декора.',
                    'price_from': price,
                    'is_active': True,
                    'is_featured': featured,
                    'order': index,
                },
            )
            self.attach_image(product, 'main_image', image, image)
            self.create_weights(product, price)
            self.create_gallery(product)

        for index, image in enumerate(['hero-slide-1.jpg', 'hero-slide-2.jpg', 'hero-slide-3.jpg']):
            slide, _ = HeroSlide.objects.update_or_create(
                order=index,
                defaults={
                    'eyebrow': 'БУТИК ДЕСЕРТОВ',
                    'title': 'Авторские торты и десерты в нежной эстетике',
                    'subtitle': 'Нежные торты, десерты, конфеты и подарочные наборы ручной работы для семейных праздников, свадеб и особенных событий.',
                    'primary_button_text': 'Смотреть каталог',
                    'primary_button_url': '#catalog',
                    'secondary_button_text': 'Оставить заявку',
                    'secondary_button_url': '#order',
                    'is_active': True,
                },
            )
            self.attach_image(slide, 'image', image, image)

        self.stdout.write(self.style.SUCCESS('Demo data loaded.'))

    def attach_image(self, instance, field_name, source_name, upload_name):
        field = getattr(instance, field_name)
        if field:
            return
        source_path = settings.BASE_DIR / 'static' / 'assets' / source_name
        if not source_path.exists():
            return
        with source_path.open('rb') as source:
            field.save(upload_name, File(source), save=True)

    def create_weights(self, product, base_price):
        weights = [
            (Decimal('1.00'), base_price, True),
            (Decimal('1.50'), base_price * Decimal('1.5'), False),
            (Decimal('2.00'), base_price * Decimal('2'), False),
            (Decimal('2.50'), base_price * Decimal('2.5'), False),
            (Decimal('3.00'), base_price * Decimal('3'), False),
            (Decimal('4.00'), base_price * Decimal('4'), False),
        ]
        for index, (weight, price, is_default) in enumerate(weights):
            ProductWeightOption.objects.update_or_create(
                product=product,
                weight=weight,
                weight_unit=ProductWeightOption.WeightUnit.KG,
                defaults={'price': price, 'is_default': is_default, 'order': index},
            )

    def create_gallery(self, product):
        for index, image in enumerate(['cake.jpg', 'hero-slide-1.jpg', 'hero-slide-2.jpg']):
            if product.images.filter(alt=f'{product.title} фото {index + 1}').exists():
                continue
            source_path = settings.BASE_DIR / 'static' / 'assets' / image
            if not source_path.exists():
                continue
            product_image = ProductImage(product=product, alt=f'{product.title} фото {index + 1}', order=index)
            with source_path.open('rb') as source:
                product_image.image.save(f'{product.slug}-{image}', File(source), save=True)
