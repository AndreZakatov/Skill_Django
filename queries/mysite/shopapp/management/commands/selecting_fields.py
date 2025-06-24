from django.contrib.auth.models import User
from django.core.management import BaseCommand

from typing import Sequence
from django.db import transaction
from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo selected fields")
        user_info =  User.objects.values("username", "pk")
        for user in user_info:
            print(user)
        self.stdout.write("Done")    
