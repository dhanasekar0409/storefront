from django.shortcuts import render
from .tasks import notify_customers


# transaction
def say_hello(request):
    notify_customers.delay("Hello")
    return render(request, "hello.html", {"name": "Dhana"})
