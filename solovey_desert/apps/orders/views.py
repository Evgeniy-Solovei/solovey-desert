from django.views.generic import TemplateView


class CartView(TemplateView):
    template_name = 'orders/cart.html'

# Create your views here.
