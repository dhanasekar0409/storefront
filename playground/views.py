from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from store.models import OrderItem, Product, Order


# transaction
def say_hello(request):
    with transaction.atomic():
        order = Order()
        order.pk = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.pk = 1
        item.quantity = 1
        item.unit_price = None  # type: ignore
        item.save()

    query_set = Product.objects.values()
    list(query_set)

    return render(request, "hello.html", {"name": "Mosh", "products": list(query_set)})
