from django.urls import path
from .views import shop_apps, groups_list, products_list, orders_list

app_name = 'shopapp'

urlpatterns = [
    path('', shop_apps, name='product_list'),
    path("groups/", groups_list, name='groups_list'),
    path("products/", products_list, name='product_list'),
    path("orders/", orders_list, name='orders_list')
]