from django.urls import path
from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product_detail/<int:pk>', views.ProductDetailView.as_view(), name='product_detail')
]
