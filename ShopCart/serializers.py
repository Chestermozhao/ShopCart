from ShopCart.models import Order, Product, Shop
from rest_framework import serializers
from django.db import transaction


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "qty",
            "product",
        ]

    def create(self, validated_data):
        qty = validated_data["qty"]
        product = validated_data["product"]
        with transaction.atomic():
            product.stock_pcs -= qty
            product.save()
            order_instance = Order.objects.create(**validated_data)
        return order_instance


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ShopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"
