from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .models import Product, Order


def shop_apps(request: HttpRequest):
    PRODUCTS = [
        {"name": "MacBook", "type": "laptop", "price": 2999},
        {"name": "ThinkPad", "type": "laptop", "price": 799},
        {"name": "MacBook Pro", "type": "laptop", "price": 3999},
        {"name": "IPhone 14 Pro", "type": "smartphone", "price": 999},
        {"name": "IPhone xr", "type": "smartphone", "price": 200},
        {"name": "Xiaomi m3t590pro super puper max XLL", "type": "smartphone", "price": 2000},
        {"name": "PC intel 10500f", "type": "desktop", "price": 670},
        {"name": "RTX 4090 TI", "type": "desktop", "price": 1670},
    ]

    device_type = request.GET.get("type")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    filter_product = PRODUCTS

    if device_type:
        filter_product = [product for product in PRODUCTS if product["type"] == device_type]

    if min_price:
        filter_product = [product for product in PRODUCTS if product["price"] >= int(min_price)]

    if min_price:
        filter_product = [product for product in PRODUCTS if product["price"] <= int(max_price)]

    return render(request, "shopapp/first_page.html", {"products": filter_product})


def groups_list(request: HttpRequest):
    context = {
        "groups": Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context=context)


def products_list(request:HttpRequest):
    context = {
        "products": Product.objects.all(),
    }
    return render(request, 'shopapp/product_list.html', context=context)

def orders_list(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user").all(),
    }
    return render(request, 'shopapp/orders_list.html', context=context)