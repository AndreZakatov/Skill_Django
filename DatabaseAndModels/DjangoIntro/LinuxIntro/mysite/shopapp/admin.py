from django.contrib import admin

from .models import Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "price", "description_short", "discount"
    list_display_links = "pk", "name"

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."

# admin.site.register(Product, ProductAdmin)

