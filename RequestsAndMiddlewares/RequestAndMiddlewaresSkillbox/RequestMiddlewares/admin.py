from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Product, Order


@admin.action(description="Archive products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description="Unarchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [mark_archived, mark_unarchived]
    list_display = "pk", "name", "description", "price", "discount", "archived"
    list_display_links = "pk", "price"
    ordering = "-name", "pk"
    search_fields = "name", ""
    fieldsets = [
        ("Товар", {
            "fields": ("name",  "description"),
            "classes": ('collapse',),
        }),
        ("Информация по цене", {
           "fields": ("discount", "price") ,
            "classes": ('collapse',),
        }),
    ]


@admin.action(description="Delivery OK")
def mark_delivery(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(delivery_status=True)


@admin.action(description="Delivery not OK")
def mark_undelivery(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(delivery_status=False)


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    actions = [mark_archived, mark_unarchived, mark_undelivery, mark_delivery]
    list_display = "pk", "user", "delivery_status", "archived", "delivery_address"
    ordering = "-delivery_status", "user"
    list_display_links = "pk", "user"
    search_fields = "delivery_address", "promocode"
    fieldsets = [
        (None, {
            "fields": ("user", "promocode", "delivery_status"),
        }),
        ("Информация по заказу", {
            "fields": ("producta",),
            "classes": ('collapse',),
        }),
    ]