import random
from .management.commands.my_generate2 import generate_name, generate_adres
from django.contrib import admin
from .models import Products, Client, Order

@admin.action(description="изменение цены")
def priceinflicion(modeladmin, request, queryset):
    queryset.update(price=random.randint(1,1000))

@admin.action(description="Изменение имени")
def name_random(modeladmin, request, queryset):
    queryset.update(name=generate_name())

@admin.action(description="Изменение адреса")
def adres_random(modeladmin, request, queryset):
    queryset.update(name=generate_adres())

class ProductsAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "quantity", "describe"]
    ordering = ["name", "price"]
    list_filter = ["name", "price"]
    search_fields = ['name', "price"]
    search_help_text = 'Поиск по полю имя, цена продукта'
    actions = [priceinflicion]
    fieldsets = [
        (
            "Название продукта",
            {
                'classes': ['wide'],
                'fields': ['name'],
            },
        ),
        (
            'Описание продукта',
            {
                'fields': ["describe"],

            }
        ),
        (
            'Подробности',
            {
                'fields': ["price", "quantity"],
            },
        )
    ]



class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", 'address']
    ordering = ["name", "phone"]
    list_filter = ["name", "phone"]
    search_fields = ['name']
    search_help_text = 'Поиск по полю Описание продукта (name)'
    actions = [name_random, adres_random]
    readonly_fields = ['phone']
    fieldsets = [
        (
            "Имя клиента",
            {
                'classes': ['wide'],
                'fields': ['name'],
            },
        ),
        (
            'Подробности',
            {
                'description': 'Адрес места жительства, почта ',
                'fields': ['address', "email"],

            }
        ),
        (
            'Секретная информация',
            {
                'classes': ['collapse'],
                'description': 'Личная информация',
                'fields':["phone"],
            },
        )
    ]

class OrderAdmin(admin.ModelAdmin):

    list_display = ["pk", "total_price", 'client']
    ordering = ["total_price", "pk"]
    list_filter = ["total_price"]

admin.site.register(Products, ProductsAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Order, OrderAdmin)