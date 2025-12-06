from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_no", "capacity", "occupied_count", "status")
    search_fields = ("room_no",)

# Register your models here.
