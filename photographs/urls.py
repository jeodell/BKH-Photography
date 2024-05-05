from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomepageView.as_view(), name="homepage"),
    path('about/', views.AboutView.as_view(), name='about'),
    path('albums/<album>/', views.get_album_view, name='album'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
