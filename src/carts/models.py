from django.db import models
from django.conf import settings
from django import forms

from products.models import Product
from checkout.models import ShippingAddress
from checkout.models import Payment


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.item.name}: {self.quantity}'

    def get_total(self):
        return round(self.item.price * self.quantity, 2)


class Order(models.Model):
    order_id = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    promo_code_applied = models.BooleanField(default=False)
    promo_code_discount = models.FloatField(default=0)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: {self.get_all_items()}'

    def get_all_items(self):
        return [item for item in self.items.all()]

    def get_total_amount(self):
        total = sum(item.get_total() for item in self.items.all())
        return total - self.promo_code_discount

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class Refund(models.Model):
    reason = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    granted = models.BooleanField(default=False)

    def __str__(self):
        return f'Refund for order {self.order.order_id}'


class RefundForm(forms.ModelForm):
    order_id = forms.CharField()

    class Meta:
        model = Refund
        fields = ['order_id', 'reason']