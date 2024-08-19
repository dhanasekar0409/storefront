from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
import requests
import logging

logger = logging.getLogger(__name__)


class HelloView(APIView):
    @method_decorator(cache_page(5 * 60))  # Cache for 5 minutes
    def get(self, request):
        try:
            logger.info("calling httpbin")
            response = requests.get("https://httpbin.org/delay/2")
            logger.info("Received response from httpbin")
            data = response.json()
        except requests.ConnectionError:
            logger.critical("httpbin is offline")
        return render(request, "hello.html", {"name": data})
