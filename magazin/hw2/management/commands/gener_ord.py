from datetime import timedelta
from django.utils import timezone
from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from hw2.models import Client, Products, Order
from random import sample, uniform, randint

from .my_generate2 import generate_name, generate_phone_number, generate_adres, genarate_product


class Command(BaseCommand):
    help = "Заполняем тестовыми данными"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('count_customers', type=int, help='количество покупателей')
        parser.add_argument('count_prods', type=int, help='количество товаров')
        parser.add_argument('count_orders', type=int, help='количество заказов')

    def handle(self, *args, **kwargs):
        count_customers = kwargs.get('count_customers')
        count_prods = kwargs.get('count_prods')
        count_orders = kwargs.get('count_orders')

        for i in range(1, count_customers + 1):
            new_name = generate_name()
            new_telefon = generate_phone_number()
            new_adres = generate_adres()
            customer = Client(name=f'{new_name}', email=f'{new_name}@mail.ru', phone=new_telefon,
                            address=new_adres)
            customer.save()


        for j in range(1, count_prods):
            new_name = genarate_product()
            product = Products(name=f'{new_name}', describe=f'description_{j}', price=uniform(10, 1000),
                               quantity=randint(1, 20))
            product.save()

        for _ in range(1, count_orders + 1):
            customer = Client.objects.filter(pk=randint(1, count_customers + 1)).first()
            product = Products.objects.filter(pk=randint(1, count_prods + 1)).first()
            self.stdout.write(f"{product}")
            dates=timezone.now() - timedelta(10)
            order = Order(client=customer, total_price=product.cost(), created=dates)
            order.save()
            order.orders.add(product)

            self.stdout.write(f"{order}")