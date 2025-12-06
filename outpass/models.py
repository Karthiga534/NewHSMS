from django.db import models
from django.conf import settings


class Outpass(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        APPROVED = "Approved", "Approved"
        REJECTED = "Rejected", "Rejected"

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='outpasses')
    reason = models.CharField(max_length=255)
    out_date = models.DateTimeField()
    expected_return = models.DateTimeField()
    actual_return = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    warden_remarks = models.TextField(blank=True, null=True)
    destination = models.CharField(max_length=255, default="")
    contact_number = models.CharField(max_length=20, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def is_late(self) -> bool:
        return bool(self.actual_return and self.actual_return > self.expected_return)

    def __str__(self) -> str:
        return f"Outpass #{self.id} - {self.student} - {self.status}"

# Create your models here.
