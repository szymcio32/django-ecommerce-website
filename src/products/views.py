from django.views.generic import ListView, DetailView
from .models import Product


class HomePage(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    paginate_by = 4


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_details.html'