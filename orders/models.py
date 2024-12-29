from django.db import models
from django.contrib.auth.models import User
from django.apps import apps


#from products.models import Product  


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_history", null=True, default=None)
    order_number = models.CharField(max_length=32, unique=True, null=False, blank=False, default="TEMP_ORDER_NUMBER")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"Order #{self.order_number}"

class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lineitems')
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} (x{self.quantity})"