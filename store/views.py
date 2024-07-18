from itertools import product
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Collection1, OrderItem, Product, Review
from .serializers import Collection1Serializer, ProductSerializer, ReviewSerializer
from django.db.models import Count


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get("collection_id")  # type: ignore
        if collection_id is not None:
            queryset = queryset.filter(collection_id=collection_id)
        return queryset

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:  # type: ignore
            return Response(
                {
                    "error": "Product can not be deleted because it is associated with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class Collection1ViewSet(ModelViewSet):
    queryset = Collection1.objects.annotate(products_count=Count("products")).all()
    serializer_class = Collection1Serializer

    def destroy(self, request, *args, **kwargs):
        collection = Collection1.objects.annotate(products_count=Count("products"))
        if collection.products.count() > 0:  # type: ignore
            return Response(
                {
                    "error": "Collection can not be deleted because it is associated with products"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}
