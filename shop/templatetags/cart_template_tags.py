from django import template

from ..models import Customer, OrderItem

register = template.Library()


@register.filter
def cart_item_count(request):
    try:
        customer = Customer.objects.get(
            device=request.COOKIES['device'], ordered=False)
        order_items = OrderItem.objects.filter(user=customer, ordered=False)
        count = 0
        for order_item in order_items:
            count += order_item.quantity
        return count
    except Exception:
        return 0
