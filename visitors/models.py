from django.db import models
from django.conf import settings


class Visitor(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visitors')
    visitor_name = models.CharField(max_length=120)
    purpose = models.CharField(max_length=200)
    in_time = models.DateTimeField()
    out_time = models.DateTimeField(blank=True, null=True)
    id_proof = models.CharField(max_length=120)

    def __str__(self) -> str:
        return f"{self.visitor_name} -> {self.student}"

# Create your models here.
