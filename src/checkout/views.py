from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string

from carts.models import Order
from .models import ShippingAddressForm
from .models import PromotionCodeForm
from .models import PromotionCode
from .models import ShippingAddress
from .models import Payment

import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, ordered=False).first()
        if not order:
            return redirect('checkout:checkout')
        order_items = order.get_all_items()
        shipping_address = ShippingAddress.objects.filter(user=self.request.user, current_address=True)
        shipping_address = shipping_address.first() if shipping_address.exists() else None
        form = ShippingAddressForm(instance=shipping_address)
        promo_form = PromotionCodeForm()
        context = {
            'order': order,
            'order_items': order_items,
            'form': form,
            'promo_form': promo_form
        }
        return render(self.request, 'checkout/checkout.html', context)

    def post(self, *args, **kwargs):
        form = ShippingAddressForm(self.request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = self.request.user
            shipping_address.save()
            order = Order.objects.filter(user=self.request.user, ordered=False).first()
            order.shipping_address = shipping_address
            order.save()
            if form.cleaned_data['save_address']:
                current_shipping_address = ShippingAddress.objects.filter(user=self.request.user, current_address=True).first()
                if current_shipping_address:
                    current_shipping_address.current_address = False
                    current_shipping_address.save()
                shipping_address.pk = None
                shipping_address.current_address = True
                shipping_address.save()
        return redirect('checkout:payment')


class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, ordered=False).first()
        return render(self.request, 'checkout/payment.html', {'order': order})

    def post(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, ordered=False).first()
        token = self.request.POST.get('stripeToken')
        try:
            charge = stripe.Charge.create(
              amount=round(float(order.get_total_amount() * 100)),
              currency="usd",
              source=token
            )
        except stripe.error.CardError:
            messages.error(self.request, 'Payment could not be made')
            return redirect('products:home-page')
        except Exception:
            messages.error(self.request, 'Internal server error')
            return redirect('products:home-page')

        payment = Payment(
            user=self.request.user,
            stripe_id=charge.id,
            amount=order.get_total_amount()
        )
        payment.save()
        order.order_id = get_random_string(length=20)
        order.payment = payment
        order.ordered = True
        order.save()

        messages.info(self.request, 'Payment was successfully issued')
        return redirect('checkout:checkout-success')


class ShippingAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    form_class = ShippingAddressForm
    template_name = 'checkout/profile.html'
    success_message = "The address has been successfully updated"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.current_address = True
        return super().form_valid(form)

    def get_object(self):
        obj = ShippingAddress.objects.filter(user=self.request.user, current_address=True)
        return obj.first() if obj.exists() else None


class PromoCodeView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
            form = PromotionCodeForm(self.request.POST)
            if form.is_valid():
                order = Order.objects.filter(user=self.request.user, ordered=False).first()
                if order.promo_code_applied:
                    messages.warning(self.request, "The promotion code has been already applied")
                    return redirect('checkout:checkout')
                try:
                    code = PromotionCode.objects.get(code=form.cleaned_data.get('code'))
                except PromotionCode.DoesNotExist:
                    messages.warning(self.request, "Provided code does not exists")
                    return redirect('checkout:checkout')
                order.promo_code_discount = order.get_total_amount() * code.percentage_discount
                order.promo_code_applied = True
                order.save()
                return redirect('checkout:checkout')


def checkout_success(request):
    return render(request, 'checkout/success.html')