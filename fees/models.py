from django.db import models
from django.conf import settings


class Fee(models.Model):
    class Status(models.TextChoices):
        PAID = "Paid", "Paid"
        UNPAID = "Unpaid", "Unpaid"

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fees')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.UNPAID)

    def __str__(self) -> str:
        return f"{self.student} - {self.status} ({self.paid_amount}/{self.total_amount})"

# Create your models here.
