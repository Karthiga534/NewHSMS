from django.db import models


class Room(models.Model):
    room_no = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField(default=1)
    occupied_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default='Vacant')  # Vacant/Occupied/Partial

    def has_vacancy(self) -> bool:
        return self.occupied_count < self.capacity

    def __str__(self) -> str:
        return f"Room {self.room_no} ({self.occupied_count}/{self.capacity})"

# Create your models here.
