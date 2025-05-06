from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Product
from shopapp.models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create order")
        user = User.objects.get(username="zakatov")
        order = Order.objects.get_or_create(
            delivery_address="Lytkarino, nabereznay",
            promocode="SALE",
            user=user,
        )
        self.stdout.write(f"Create_order {order}")