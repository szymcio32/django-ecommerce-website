from django.contrib import admin

from .models import OrderItem
from .models import Order
from .models import Refund


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'payment',
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'payment',
    ]
    list_filter = ['ordered',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'order_id'
    ]
    actions = [make_refund_accepted]


admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Refund)
