from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]

    name = models.CharField(max_length=200)
    description= models.TextField(null=False,
                                  blank=True)
    price = models.DecimalField(default=0,
                                max_digits=8,
                                decimal_places=2,
                                validators=[MinValueValidator(0),
                                ])
    discount = models.PositiveSmallIntegerField(default=0,
                                                validators=[MaxValueValidator(100)])
    create_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)


    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"


class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    producta = models.ManyToManyField(Product, related_name="orders")
    delivery_status = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
