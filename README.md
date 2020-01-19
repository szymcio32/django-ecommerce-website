# Django e-commerce website

E-commerce website built with Django. It has following functionality:
- user registration
- add / change user billing address
- add / remove item from cart
- change the default billing address during the checkout process
- apply a promotion code during the checkout process
- pay for a order using Stripe
- list all proceeded orders
- request a refund for a order

The purpose of this project was to learn Django Framework.

## Setup

- Create and activate virtual environment
```buildoutcfg
python -m venv venv
```
- Create a .env file in e-commerce-django-website directory with following variables.
Credentials for email should be taken from your mailtrap account
```buildoutcfg
STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```
- Add STRIPE_PUBLISHABLE_KEY into stripe_payment.js file
- Install packages from requirements.txt
```buildoutcfg
pip install -r requirements.txt
```
- Run command
```buildoutcfg
python src\manage.py runserver
```

## Example of app
Home page

![home-page](https://user-images.githubusercontent.com/32844693/67404105-27f79980-f5b3-11e9-9f9f-d8e7a9e8c401.PNG)

Product details page

![product-detail](https://user-images.githubusercontent.com/32844693/67404107-28903000-f5b3-11e9-9a02-e2767525eb69.PNG)

Shipping address form page

![shipping-address](https://user-images.githubusercontent.com/32844693/67404108-28903000-f5b3-11e9-9d68-a17805ac4efa.PNG)

Refund page

![refund-page](https://user-images.githubusercontent.com/32844693/67404109-28903000-f5b3-11e9-8650-88c071e2e605.PNG)

Cart page

![cart](https://user-images.githubusercontent.com/32844693/67404274-6b520800-f5b3-11e9-80fc-c9db7c7bb732.PNG)

Checkout page

![checkout-page-without-code](https://user-images.githubusercontent.com/32844693/67404275-6bea9e80-f5b3-11e9-8c98-8c6ae9397f46.PNG)

Checkout page with discount code

![checkout-page-with-code](https://user-images.githubusercontent.com/32844693/67404278-6bea9e80-f5b3-11e9-91a7-be595b128732.PNG)

Payment page

![payment](https://user-images.githubusercontent.com/32844693/67404276-6bea9e80-f5b3-11e9-94ec-5a9e2215cf55.PNG)

Success order page

![success-page](https://user-images.githubusercontent.com/32844693/67404277-6bea9e80-f5b3-11e9-987b-20c573e4fa74.PNG)

Orders page

![orders-list](https://user-images.githubusercontent.com/32844693/67404279-6bea9e80-f5b3-11e9-9bb3-513836cc76fc.PNG)

## Technologies

- Python 3.7
- Django 2.2
- HTML / JS
- Bootstrap 4.3.1
- Stripe API
- mailtrap.io
- AJAX