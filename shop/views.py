from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Item, Order, OrderItem, Address, Payment, Customer, IMG_SIZE_CHOICES, PRICE_CHOICES
from .forms import CheckoutForm, ImgSizeForm
import stripe
import random
import string
import json

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class ShopView(ListView):
    model = Item
    paginate_by = 4
    template_name = 'shop/shop.html'


def get_product_view(request, slug):
    if request.method == 'GET':
        form = ImgSizeForm()
        item = Item.objects.get(slug=slug)
    elif request.method == 'POST':
        item = Item.objects.get(slug=slug)
        form = ImgSizeForm(request.POST or None)
        img_size = form.cleaned_data['img_size']

    return render(request, 'shop/product.html', {
        'form': form,
        'item': item
    })


class CartView(View):
    def get(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.filter(
                device=request.COOKIES['device'], ordered=False).first()
            order = Order.objects.filter(
                user=customer, ordered=False).first()
            order_items = OrderItem.objects.filter(
                user=customer, ordered=False)
            context = {
                'order': order,
                'order_items': order_items
            }
            return render(self.request, 'shop/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'No active order found.')
            return redirect('shop')


class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.filter(
                device=request.COOKIES['device'], ordered=False).first()
            order = Order.objects.filter(
                user=customer, ordered=False).first()
            order_items = OrderItem.objects.filter(
                user=customer, ordered=False)
            form = CheckoutForm()
            context = {
                'order': order,
                'order_items': order_items,
                'form': form,
            }
            return render(self.request, 'shop/checkout.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'No active order found.')
            return redirect('shop')

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            customer = Customer.objects.get(
                device=request.COOKIES['device'], ordered=False)
            order = Order.objects.get(user=customer, ordered=False)
            if form.is_valid():
                shipping_first_name = form.cleaned_data.get(
                    'shipping_first_name')
                shipping_last_name = form.cleaned_data.get(
                    'shipping_last_name')
                email = form.cleaned_data.get('email')
                shipping_street = form.cleaned_data.get('shipping_street')
                shipping_apartment = form.cleaned_data.get(
                    'shipping_apartment')
                shipping_state = form.cleaned_data.get('shipping_state')
                shipping_zipcode = form.cleaned_data.get('shipping_zipcode')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')
                if same_billing_address:
                    billing_first_name = shipping_first_name
                    billing_last_name = shipping_last_name
                    billing_street = shipping_street
                    billing_apartment = shipping_apartment
                    billing_state = shipping_state
                    billing_zipcode = shipping_zipcode
                else:
                    billing_first_name = form.cleaned_data.get(
                        'billing_first_name')
                    billing_last_name = form.cleaned_data.get(
                        'billing_last_name')
                    billing_street = form.cleaned_data.get('billing_street')
                    billing_apartment = form.cleaned_data.get(
                        'billing_apartment')
                    billing_state = form.cleaned_data.get('billing_state')
                    billing_zipcode = form.cleaned_data.get('billing_zipcode')
                shipping_address, created_shipping = Address.objects.get_or_create(
                    first_name=shipping_first_name,
                    last_name=shipping_last_name,
                    street=shipping_street,
                    apartment=shipping_apartment,
                    state=shipping_state,
                    zipcode=shipping_zipcode,
                    same_billing_address=same_billing_address,
                    address_type='S'
                )
                billing_address, created_billing = Address.objects.get_or_create(
                    first_name=billing_first_name,
                    last_name=billing_last_name,
                    street=billing_street,
                    apartment=billing_apartment,
                    state=billing_state,
                    zipcode=billing_zipcode,
                    same_billing_address=same_billing_address,
                    address_type='B'
                )
                if created_shipping:
                    shipping_address.save()
                if created_billing:
                    billing_address.save()
                if not customer.username:
                    customer.username = f"{shipping_first_name} {shipping_last_name}"
                    customer.email = email
                    customer.save()
                elif customer.username != f"{shipping_first_name} {shipping_last_name}":
                    new_customer = Customer()
                    new_customer.username = f"{shipping_first_name} {shipping_last_name}"
                    new_customer.email = email
                    new_customer.device = request.COOKIES['device']
                    new_customer.save()
                    order.user = new_customer
                order.shipping_address = shipping_address
                order.billing_address = billing_address
                order.save()

                return redirect('payment')
            messages.warning(self.request, 'Error')
            return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, 'No active order found.')
            return redirect('shop')


class PaymentView(View):
    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(
            device=request.COOKIES['device'], ordered=False)
        order = Order.objects.get(
            user=customer, ordered=False)
        order_items = OrderItem.objects.filter(
            user=customer, ordered=False
        )
        if order.billing_address:
            context = {
                'order': order,
                'order_items': order_items
            }
            return render(self.request, 'shop/payment.html', context)
        else:
            messages.warning(self.request, 'You must add a billing address')
            return redirect('checkout')

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(
            device=request.COOKIES['device'], ordered=False)
        order = Order.objects.get(
            user=customer, ordered=False)
        amount = int(order.get_total())

        try:
            # Create a customer
            stripeCustomer = stripe.Customer.create(
                name=customer.username,
                email=customer.email,
                source=request.POST['stripeToken']
            )
            print(stripeCustomer)

            # Create a charge
            # charge = stripe.Charge.create(
            #     customer=customer,
            #     amount=amount * 100,
            #     currency='usd',
            #     source=stripeCustomer.default_source
            # )
            payment = Payment(user=customer, amount=order.get_total())
            # payment.stripe_charge_id = charge.id
            payment.save()

            order_items = order.items.filter(ordered=False)
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            customer.ordered = True
            customer.save()

            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()

            subject_customer = f'Thank you for your order from BKH Photography!'
            subject_owner = f'New order received from {customer.username}'
            message_customer = f'Thank you for your order! Your order reference code is {order.ref_code}.'
            message_owner = f'Go to /admin and see the order details under Orders'

            # EmailMessage has more options
            send_mail(subject_customer, message_customer,
                      settings.EMAIL_HOST_USER, [customer.email])

            send_mail(subject_owner, message_owner,
                      settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])

            messages.success(self.request, 'Your order has been placed.')
            return redirect('/')
        except:
            return redirect('/shop/checkout')


def add_to_cart(request, slug, img_size):
    # Get device
    device = request.COOKIES['device']
    # Get item
    item = get_object_or_404(Item, slug=slug)
    # Get img size
    if request.POST:
        img_size = request.POST['img_size']
    price = dict(PRICE_CHOICES).get(img_size)
    customer, created = Customer.objects.get_or_create(
        device=device, ordered=False)
    # Get or create OrderItem from Item
    order_item, created = OrderItem.objects.get_or_create(
        item=item, img_size=img_size, price=price, user=customer, ordered=False)
    # If Order exists, increment or add Item
    order_qs = Order.objects.filter(
        user=customer, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug, img_size=img_size).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'Item quantity updated in cart.')
        else:
            order.items.add(order_item)
            messages.info(request, 'Item added to the cart.')
    # Otherwise, create Order and add Item
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=customer, ordered_date=ordered_date)
        messages.info(request, 'Item added to the cart.')
        order.items.add(order_item)
    return redirect('cart')


def remove_from_cart(request, slug):
    # Get Item
    item = get_object_or_404(Item, slug=slug)
    # Get customer
    customer = Customer.objects.get(
        device=request.COOKIES['device'], ordered=False)
    # If Order exists, find Item and remove
    order_qs = Order.objects.filter(
        user=customer, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=customer, ordered=False)[0]
            order.items.remove(order_item)
            if order.items.count() <= 0:
                order.delete()
            order_item.delete()
            messages.info(request, 'Item removed from cart.')
        else:
            messages.info(request, 'Item not found in cart.')
    else:
        messages.info(request, 'No active order found.')
    return redirect('cart')


def remove_single_item_from_cart(request, slug):
    # Get item
    item = get_object_or_404(Item, slug=slug)
    # Get customer
    customer = Customer.objects.get(
        device=request.COOKIES['device'], ordered=False)
    # If Order exists, find Item and update quantity
    order_qs = Order.objects.filter(
        user=customer, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=customer, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, 'Item quantity updated in cart.')
            else:
                remove_from_cart(request, slug)
        else:
            messages.info(request, 'Item not found in cart.')
    else:
        messages.info(request, 'No active order found.')
    return redirect('cart')
