from django.db import models

from api.apps.authentication.models import User


class Order(models.Model):
    PIZZA_SIZES = (
        ("Small", "Small"),
        ("Medium", "Medium"),
        ("Large", "Large"),
        ("Extra-large", "Extra-large"),
    )

    ORDER_STATUSES = (
        ("Pending", "Pending"),
        ("In Transit", "In Transit"),
        ("Delivered", "Delivered"),
    )

    flavour = models.CharField(max_length=255, null=False, blank=False)
    size = models.CharField(
        max_length=12, choices=PIZZA_SIZES, default="Small"
    )
    quantity = models.IntegerField()
    status = models.CharField(
        max_length=50, choices=ORDER_STATUSES, default="Pending"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.flavour
