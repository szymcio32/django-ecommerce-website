"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from carts.views import OrdersListView
from carts.views import RefundView
from checkout.views import ShippingAddressUpdateView


urlpatterns = [
    path('', include('products.urls')),
    path('cart/', include('carts.urls')),
    path('checkout/', include('checkout.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/orders/', OrdersListView.as_view(), name='show-orders'),
    path('accounts/profile/', ShippingAddressUpdateView.as_view(), name='profile'),
    path('refund/', RefundView.as_view(), name='refund')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)