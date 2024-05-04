from datetime import datetime, timedelta
import logging
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, render
from .models import Client, Products, Order
from .forms import ImageForm, ProductForm
from django.utils import timezone

logger = logging.getLogger(__name__)

def receive_orders(request, pk_cust):
    orders = Order.objects.filter(client=pk_cust)
    client = get_object_or_404(Client, pk=pk_cust)
    products = {}
    for order in orders:
        prod_list = []
        order_prods = order.orders.all()
        for prod in order_prods:
            prod_list.append(prod.name)
        products[order.pk] = set(prod_list)
    context = {"orders": orders, "products": products, "client": client}
    return render(request, "hw2/orders.html", context)

def orders_story(request, pk_cust, days):
    customer = Client.objects.filter(pk=pk_cust).first()
    ord = Order.objects.filter(client=pk_cust)
    my_date = timezone.now() - timedelta(days=days)
    order_list = ord.filter(created__gte=my_date, created__lte=timezone.now())
    prods_dict = {}
    for order in order_list:
        prods = order.orders.all()
        prods_dict[order] = set(prods)
    context = {
        "prods_dict": prods_dict,
        "customer": customer,
        "days": days,
    }

    return render(request, "hw2/orders_story.html", context)


def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            fs.save(image.name, image)
    else:
        form = ImageForm()
    return render(request, 'hw2/upload_image.html', {'form':form})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        message = 'Ошибка в данных'
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            logger.info(f'Получили {name=}, {describe=}, {price=}, {quantity= }')
            image = form.cleaned_data['image']
            product = Products(name=name, describe=describe, price=price, quantity=quantity,
                               image=image)
            product.save()
            fs = FileSystemStorage()
            fs.save(image.name, image)
            message = 'Продукт сохранён'
    else:
        form = ProductForm()
        message = 'Заполните форму'
    return render(request, 'hw2/add_product.html', {'form':
                                                     form, 'message': message})
