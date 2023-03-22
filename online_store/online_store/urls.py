from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from online_store import settings

urlpatterns = [
    path('', include('catalog.urls')),
    path('', include('shopping_cart.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('authuser.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
