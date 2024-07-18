from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Collection1, Product
from .serializers import Collection1Serializer, ProductSerializer
from django.db.models import Count
from store import serializers


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related("collection").all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
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

class CollectionDetail(RetrieveUpdateDestroyAPIView): 
     queryset=Collection1.objects.annotate(products_count=Count('products'))
     serializer_class = Collection1Serializer
    
     def delete(self,request,pk):
       collection=Collection1.objects.annotate(products_count=Count('products'))
        if collection.products.count() > 0:  # type: ignore
            return Response(
                {
                    "error": "Collection can not be deleted because it is associated with products"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
