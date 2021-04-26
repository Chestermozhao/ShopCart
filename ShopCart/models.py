from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Shop(BaseModel):
    name = models.CharField(max_length=256, null=False)

    class Meta:
        db_table = "shop"
        ordering = ["created_at"]


class Product(BaseModel):
    id = models.AutoField(auto_created=True, primary_key=True)
    stock_pcs = models.PositiveIntegerField(null=False)
    sales = models.IntegerField(default=0)
    price = models.PositiveIntegerField(null=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    is_vip = models.BooleanField(default=False)

    class Meta:
        db_table = "products"
        ordering = ["created_at"]


class Order(BaseModel):
    id = models.AutoField(auto_created=True, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(null=False)
    price = models.PositiveIntegerField(null=False)
    customer_id = models.CharField(max_length=256, null=False)

    class Meta:
        db_table = "orders"
        ordering = ["created_at"]
