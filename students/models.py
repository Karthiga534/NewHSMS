from django.db import models
from django.conf import settings


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    name = models.CharField(max_length=120)
    reg_no = models.CharField(max_length=50, unique=True)
    room_no = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20)
    parent_contact = models.CharField(max_length=20)
    course = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    department = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name} ({self.reg_no})"

# Create your models here.
