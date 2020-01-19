from django.db import models
from django import forms
from django_countries.fields import CountryField
from django.urls import reverse
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    country = CountryField()
    phone = models.CharField(max_length=30)
    current_address = models.BooleanField(default=False)

    def __str__(self):
        return f'Shipping address for {self.user.username}: {self.street} {self.street_number}, {self.city}'

    def get_absolute_url(self):
        return reverse('profile')


class ShippingAddressForm(forms.ModelForm):
    save_address = forms.BooleanField(required=False, label='Save the billing addres')

    class Meta:
        model = ShippingAddress
        fields = [
            'first_name',
            'last_name',
            'street',
            'street_number',
            'zip_code',
            'city',
            'country',
            'phone'
        ]


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_id = models.CharField(max_length=60)
    amount = models.FloatField()
    issued_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} payment: {self.amount}'


class PromotionCode(models.Model):
    code = models.CharField(max_length=50)
    percentage_discount = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    def __str__(self):
        return self.code


class PromotionCodeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].required = False

    class Meta:
        model = PromotionCode
        fields = ['code']
        labels = {
            'code': 'Promotion Code'
        }
