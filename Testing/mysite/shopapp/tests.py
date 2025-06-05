from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from django.conf import settings
from string import ascii_letters
from random import choices

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from shopapp.models import Product, Order


class ProductCreateViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=cls.product_name)

    def test_create_product(self):
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "123.33",
                "description": "God table",
                "discount": "10",
            }
        )
        self.assertRedirects(response, reverse("shopapp:product_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name)
        )


class ProductDetailsViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Best")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_product(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductListViewTestCase(TestCase):
    fixtures = [
        "products-fixture.json",
    ]

    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"))
        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="Bob", password="1234567890987654321")
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_orders_view_nor_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.credential = dict(username="Bob", password="1234567890987654321")
        cls.user = User.objects.create_user(**cls.credential)
        content_type = ContentType.objects.get_for_model(Order)
        permission = Permission.objects.get(
            content_type=content_type,
            codename='view_order',
        )
        cls.user.user_permissions.add(permission)

        # Создание продукта
        cls.product = Product.objects.create(
            name="test product for orders",
            description="Product for test order",
            price=777,
            discount=10,
        )

        cls.order = Order.objects.create(
            delivery_address = "Test address puplin hous",
            promocode = "TESTFORTEST",
            user = cls.user,
        )
        cls.order.products.add(cls.product)

    @classmethod
    def tearDownClass(cls):
        cls.order.delete()
        cls.product.delete()
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_order_details(self):
        response = self.client.get(
            reverse("shopapp:order_details", kwargs={"pk": self.order.pk})
        )
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        
        # Проверяем, что в контексте тот же заказ
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"].pk, self.order.pk)

 
