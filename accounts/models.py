from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Roles(models.TextChoices):
        STUDENT = "student", "Student"
        WARDEN = "warden", "Warden"
        ADMIN = "admin", "Admin"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.STUDENT,
        help_text="Role for role-based access control",
    )

    reg_no = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Registration number for students (optional for staff)",
        unique=False,
    )

    def __str__(self) -> str:  # type: ignore[override]
        display = self.username
        if self.reg_no:
            display = f"{display} ({self.reg_no})"
        return display

# Create your models here.
