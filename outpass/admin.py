from django.contrib import admin
from .models import Outpass


@admin.register(Outpass)
class OutpassAdmin(admin.ModelAdmin):
    list_display = ("student", "out_date", "expected_return", "actual_return", "status")
    list_filter = ("status",)
    search_fields = ("student__username", "student__reg_no")

# Register your models here.
