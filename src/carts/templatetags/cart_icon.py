from django import template
from carts.models import Order


register = template.Library()


@register.filter
def total_cart_items(user):
    if user.is_authenticated:
        order = Order.objects.filter(user=user, ordered=False).first()
        return order.get_total_quantity() if order else 0
    return 0
