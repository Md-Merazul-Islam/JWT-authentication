from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Payment(models.Model):
    user = models.ForeignKey(
        User, related_name='payments', null=True, blank=True, on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False
    )
    payment_intent_id = models.CharField(
        max_length=255, null=True, blank=True, unique=True
    )
    currency = models.CharField(max_length=10, default="usd")
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment ID: {self.payment_id}, Amount: {self.amount}'
