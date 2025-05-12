from django.core.management import BaseCommand

from shopapp.models import Order, Product

class Command(BaseCommand):
    def handle(self, *args, **options):
        order = Order.objects.first()
        if not order:
            self.stdout.write("No orders found")
            return

        products = Product.objects.all()

        for product in products:
            order.producta.add(product)

        order.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added products {order.producta.all()} to order {order}"
            )
        )