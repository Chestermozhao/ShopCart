import arrow
import csv
from datetime import datetime, timedelta

from django.db.models import Count, Sum

from backend.factory import create_app


app = create_app()


CSV_HEADER = ["shop_id", "qty", "price", "total"]


def get_file_name():
    last_date = arrow.now().shift(days=-1).format("YYYY-MM-DD")
    return f"{last_date}-order-list-by-shops.csv"


@app.task(ignore_result=True)
def report():
    from ShopCart.models import Order, Shop

    orders = (
        Order.objects.filter(created_at__gte=datetime.now() - timedelta(days=1))
        .values("shop_id")
        .annotate(qty=Sum("qty"), price=Sum("price"), total=Count("shop_id"))
        .all()
    )

    file_name = get_file_name()

    with open(file_name, "w", encoding="utf-8", newline="") as f:
        f_csv = csv.writer(f)
        f_csv = csv.DictWriter(f, CSV_HEADER)
        f_csv.writeheader()

        for order in orders:
            order["shop_id"] = Shop.objects.get(id=order["shop_id"]).name
            f_csv.writerow(order)
