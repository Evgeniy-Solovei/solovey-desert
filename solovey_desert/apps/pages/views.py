from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView

from apps.catalog.models import Category, Product
from apps.pages.models import HeroSlide


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero_slides'] = HeroSlide.objects.filter(is_active=True).order_by('order', 'id')
        context['categories'] = Category.objects.filter(is_active=True, is_featured=True).order_by('order', 'title')
        context['featured_products'] = (
            Product.objects.filter(is_active=True, is_featured=True)
            .select_related('category')
            .prefetch_related('weight_options')
            .order_by('order', 'title')[:12]
        )
        context['seo_title'] = 'Solovey Desert - авторские торты и десерты в Минске'
        context['seo_description'] = settings.SITE_DESCRIPTION
        context['seo_canonical'] = self.request.build_absolute_uri(reverse('pages:home'))
        return context


class RobotsTxtView(TemplateView):
    content_type = 'text/plain'

    def get(self, request, *args, **kwargs):
        lines = [
            'User-agent: *',
            'Disallow: /admin/',
            'Disallow: /api/',
            'Disallow: /cart/',
            '',
            f'Sitemap: {settings.SITE_URL}/sitemap.xml',
            '',
        ]
        return HttpResponse('\n'.join(lines), content_type=self.content_type)

