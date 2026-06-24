from django.db import models
from offers_app.models import OffersDetails
from django.contrib.auth import get_user_model

User = get_user_model()


class Orders(models.Model):
    """Represents an order placed by a customer for a specific offer detail tier.
    Tracks which customer placed the order, which business user receieves it and its current status."""

    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=50, null=False, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='customer_orders')
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='business_orders')
    offer_detail = models.ForeignKey(
        OffersDetails, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.status}"
