from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "reg_no", "room_no", "course", "year", "department")
    search_fields = ("name", "reg_no", "room_no", "course", "department")

# Register your models here.
