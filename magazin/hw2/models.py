from django.db import models
from datetime import datetime


class Client(models.Model):
    name = models.CharField(max_length=64, blank=False)
    email = models.EmailField(blank=False)
    phone = models.CharField(max_length=12)
    address = models.TextField()
    register_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Покупатель - {self.name}, эл. почта: {self.email}"


class Products(models.Model):
    name = models.CharField(max_length=100, blank=False)
    describe = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product_images', default='default_image.jpg')

    def cost(self):
        prod_cost = self.price * self.quantity
        return prod_cost

    def __str__(self):
        return f"продукт {self.name} общей стоимостью {self.cost()}"


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders")
    orders = models.ManyToManyField(Products, related_name="in_order")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"клиент {self.client.name}\nномер заказа {self.id},  стоимость {self.total_price}"

