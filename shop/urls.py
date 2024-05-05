from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.ShopView.as_view(), name='shop'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('<slug>/', views.get_product_view, name='product'),
    path(r'add-to-cart/<slug>/<img_size>/',
         views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>',
         views.remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>',
         views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
