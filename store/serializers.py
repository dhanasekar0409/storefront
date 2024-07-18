from rest_framework import serializers
from decimal import Decimal
from store.models import Collection1, Product


class Collection1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Collection1
        fields = ["id", "title", "products_count"]

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "slug",
            "inventory",
            "unit_price",
            "price_with_tax",
            "collection",
        ]

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    #  collection = CollectionSerializer()
    #  collection = serializers.HyperlinkedRelatedField(
    #      queryset=Collection1.objects.all(), view_name="collection-detail"
    #  )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
