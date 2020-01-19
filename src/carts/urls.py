from django.urls import path
from .views import increase_product_in_cart, remove_from_cart, decrease_product_in_cart, CartDetailView, AddToCartAjax


app_name = "carts"

urlpatterns = [
    path('', CartDetailView.as_view(), name='show-cart'),
    path('add/<int:product_id>/', AddToCartAjax.as_view(), name='add-to-cart'),
    path('increase/<int:product_id>/', increase_product_in_cart, name='increase-product-in-cart'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove-from-cart'),
    path('decrease/<int:product_id>/', decrease_product_in_cart, name='decrease-product-in-cart')
]
