from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from .models import Collection1, Product
from .serializers import Collection1Serializer, ProductSerializer
from django.db.models import Count


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related("collection").all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if request.method == "GET":
            serializer = ProductSerializer(product)
            return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:  # type: ignore
            return Response(
                {
                    "error": "Product can not be deleted because it is associated with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Collection1List(ListCreateAPIView):
    queryset = Collection1.objects.annotate(products_count=Count("products")).all()
    serializer_class = Collection1Serializer


@api_view(["GET", "POST", "DELETE"])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection1.objects.annotate(products_count=Count("products")), pk=pk
    )

    if request.method == "GET":
        serializer = Collection1Serializer(collection)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = Collection1Serializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        if collection.products.count() > 0:  # type: ignore
            return Response(
                {
                    "error": "Collection can not be deleted because it is associated with products"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
