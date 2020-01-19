from django.contrib import admin

from .models import Category
from .models import Product

admin.site.register(Category)
admin.site.register(Product)