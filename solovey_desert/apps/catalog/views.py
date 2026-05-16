from django.views.generic import DetailView

from .models import Category, Product


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'catalog/category_detail.html'
    context_object_name = 'category'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Category.objects.filter(is_active=True).prefetch_related('products__weight_options')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        context['seo_title'] = f'{category.title} - заказать десерты в Минске | Solovey Desert'
        context['seo_description'] = category.description or f'{category.title}: авторские десерты ручной работы в Минске.'
        context['seo_canonical'] = self.request.build_absolute_uri(category.get_absolute_url())
        if category.image:
            context['seo_image'] = self.request.build_absolute_uri(category.image.url)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True)
            .select_related('category')
            .prefetch_related('images', 'weight_options')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['seo_title'] = f'{product.title} - заказать в Минске | Solovey Desert'
        context['seo_description'] = product.short_description or product.description or f'{product.title}: авторский десерт ручной работы.'
        context['seo_canonical'] = self.request.build_absolute_uri(product.get_absolute_url())
        if product.main_image:
            context['seo_image'] = self.request.build_absolute_uri(product.main_image.url)
        return context
