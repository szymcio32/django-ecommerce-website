from django.contrib import admin

from .models import ShippingAddress
from .models import Payment
from .models import PromotionCode

admin.site.register(ShippingAddress)
admin.site.register(Payment)
admin.site.register(PromotionCode)