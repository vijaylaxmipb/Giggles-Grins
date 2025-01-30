from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class UserOrder(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="order_history",
        null=True,
        default=None)
    order_number = models.CharField(
        max_length=32,
        unique=True,
        null=False,
        blank=False,
        default="TEMP_ORDER_NUMBER")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")

    def update_total(self):
        """
        Update total price for the order based on line items.
        """
        # Aggregate the sum of all line item totals
        self.total_price = self.details.aggregate(
            Sum('lineitem_total')
        )['lineitem_total__sum'] or 0

        # Save the updated total
        self.save()

        # Debugging output
        print(f"Updated total for Order #{self.order_number}: {self.total_price}")

    def __str__(self):
        return f"Order #{self.order_number}"

class OrderDetail(models.Model):  
    order = models.ForeignKey(
        UserOrder,
        on_delete=models.CASCADE,
        related_name='details')  # Updated to UserOrder
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2)

    def save(self, *args, **kwargs):
        """
        Override save method to update lineitem_total and the order total.
        """
        if not self.lineitem_total:
            raise ValueError("lineitem_total must be explicitly set.")

        super().save(*args, **kwargs)

        self.order.update_total()

    def __str__(self):
        return f"{self.product_name} (x{self.quantity})"