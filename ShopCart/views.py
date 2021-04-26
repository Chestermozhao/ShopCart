from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.response import Response

from ShopCart.serializers import OrderSerializer, ProductSerializer, ShopSerializer
from ShopCart.models import Product, Order, Shop
from libs.decorators import inventory_checker, is_auth, delete_order_checker


class IndexView(View):
    """
    main page template
    """

    def get(self, request):
        products = Product.objects.all()
        orders = Order.objects.all()
        return render(request, "base.html", {"products": products, "orders": orders})


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class TopProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request):
        """
        Get top3 saled products and notidy with ids_arr
        """
        products = Product.objects.filter(sales__gt=0).order_by("-sales")[:3]
        top_product_ids = [product.id for product in products]
        messages.info(request, top_product_ids)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @method_decorator(is_auth)
    @method_decorator(inventory_checker)
    def create(self, request):
        """
        Create order with post method

        :param quantity: int
        :param product_id: int
        :param customer_id: int
        """
        count = int(request.POST["quantity"])
        product_id = request.POST["product_id"]
        customer_id = request.POST["customer_id"]

        product = Product.objects.select_for_update().get(id=product_id)

        shop = Shop.objects.get(id=product.shop_id)
        if not shop:
            messages.error(request, "商店不存在")
            return redirect("index")
        order = Order.objects.create(
            product=product,
            customer_id=customer_id,
            qty=count,
            price=count * product.price,
            shop=shop,
        )
        product.sales += count
        product.stock_pcs -= count
        with transaction.atomic():
            product.save()
            order.save()
        messages.info(request, "訂單創建成功")
        return redirect("index")

    @method_decorator(delete_order_checker)
    def destroy(self, request, *args, **kwargs):
        """
        Delete order with primary key

        :param pk: int
        """
        pk = kwargs["pk"]
        order = Order.objects.get(pk=pk)
        product = Product.objects.get(pk=order.product.id)
        product.stock_pcs += order.qty
        product.sales -= order.qty
        with transaction.atomic():
            product.save()
            order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
