from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from ShopCart.models import Product, Order


def inventory_checker(func):
    def wrapper(request, *args, **kwargs):
        count = request.POST.get("quantity", None)
        product_id = request.POST.get("product_id", None)
        product = Product.objects.get(id=product_id)
        if not product:
            messages.error(request, "商品不存在")
            return redirect("index")
        if int(count) > product.stock_pcs:
            messages.error(request, "貨源不足")
            return redirect("index")
        return func(request, *args, **kwargs)

    return wrapper


def delete_order_checker(func):
    def wrapper(request, *args, **kwargs):
        order_id = kwargs["pk"]
        order = Order.objects.get(id=order_id)
        if not order:
            messages.error(request, "訂單不存在")
            return redirect("index")
        product = Product.objects.filter(id=order.product_id).first()
        if not product:
            messages.error(request, "商品不存在")
            return redirect("index")
        if product.stock_pcs == 0:
            messages.info(request, "商品到貨")
        return func(request, *args, **kwargs)

    return wrapper


def is_auth(func):
    def wrapper(request, *args, **kwargs):
        is_vip = request.POST.get("is_vip", None)
        product_id = request.POST.get("product_id", None)
        product = get_object_or_404(Product, id=product_id)
        if all([product.is_vip, not is_vip]):
            messages.error(request, "權限不足")
            return redirect("index")
        else:
            return func(request, *args, **kwargs)

    return wrapper
