from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User

IMG_SIZE_CHOICES = (
    ('5R', '5x7'),
    ('8R', '8x10'),
    ('11R', '11x14'),
    ('12S', '12x12'),
    ('16R', '16x20'),
    ('16S', '16x16'),
    ('18R', '18x24'),
    ('20R', '20x30'),
)

PRICE_CHOICES = (
    ('5R', '15'),
    ('8R', '20'),
    ('11R', '30'),
    ('12S', '25'),
    ('16R', '40'),
    ('16S', '35'),
    ('18R', '50'),
    ('20R', '65'),
)


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    device = models.CharField(max_length=100, null=True, blank=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        if self.username:
            return self.username
        else:
            return self.email


class Item(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='images/shop', null=True)
    price = models.CharField(max_length=3, choices=PRICE_CHOICES, default='5R')
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_price_as_float(self):
        return float(dict(PRICE_CHOICES).get(self.price))

    def get_price_choices(self):
        return PRICE_CHOICES

    def get_img_size_choices(self):
        return IMG_SIZE_CHOICES

    def update_price(self, price):
        self.price = price
        return

    def get_absolute_url(self):
        return reverse('product', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={
            'slug': self.slug,
        })

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(Customer,
                             on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    img_size = models.CharField(
        max_length=3, choices=IMG_SIZE_CHOICES, default='5R')
    price = models.FloatField(null=True)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.price

    class Meta:
        ordering = ['-item']


class Order(models.Model):
    user = models.ForeignKey(Customer,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    shipped = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total


class Address(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    apartment = models.CharField(
        max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100)
    country = models.CharField(
        max_length=100, default='United States')
    zipcode = models.IntegerField()

    def __str__(self):
        return f"{self.street} {self.state}, {self.country} {self.zipcode}"

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    user = models.ForeignKey(Customer,
                             on_delete=models.CASCADE, blank=True, null=True)
    order_ref_code = models.CharField(max_length=20, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=100)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
