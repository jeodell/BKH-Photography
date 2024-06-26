from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail

from .models import Address, Customer, Item, Order, OrderItem, Payment


def order_shipped(mdoeladmin, request, queryset):
    queryset.update(shipped=True, delivered=False)
    subject = 'Your order from Brianna Haferman Photography has been shipped!'
    message = f'We did it! Your prints are on their way!\n\nOrder {queryset[0].ref_code} is being sent to {queryset[0].shipping_address}.\nPlease let us know if any of this information needs to be updated.\n\nThank you again for your support!\nBrianna Haferman'
    customer_email = queryset[0].user.email
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [customer_email])
    except Exception:
        print('Could not send email to customer.')


def order_delivered(modeladmin, request, queryset):
    queryset.update(shipped=False, delivered=True)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'img', 'slug')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_per_page = 25


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'img_size', 'price', 'quantity', 'ordered')
    list_display_links = ('user', 'item')
    list_filter = ('ordered',)
    search_fields = ('user__username', 'item')
    list_per_page = 25


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'ref_code',
                    'shipping_address', 'ordered', 'shipped', 'delivered')
    list_display_links = ('user',)
    list_filter = ('ordered', 'shipped', 'delivered')
    search_fields = ('user__username', 'ref_code')
    list_per_page = 25
    actions = [order_shipped, order_delivered]


class AddressAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'street', 'apartment', 'state',
                    'country', 'zipcode')
    list_display_links = ('first_name',
                          'last_name', 'street')
    search_fields = ('first_name', 'last_name')
    list_per_page = 25


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'device', 'ordered')
    list_display_links = ('username', 'email', 'device')
    search_fields = ('username', 'email')
    list_per_page = 25


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_ref_code',
                    'stripe_charge_id', 'amount', 'timestamp')
    list_display_links = ('user', 'stripe_charge_id')
    search_fields = ('user', 'order_ref_code', 'stripe_charge_id')
    list_per_page = 25


admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Customer, CustomerAdmin)
