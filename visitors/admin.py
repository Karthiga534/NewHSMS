from django.contrib import admin
from .models import Visitor


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("visitor_name", "student", "in_time", "out_time", "id_proof")
    list_filter = ("in_time",)
    search_fields = ("visitor_name", "student__username")

# Register your models here.
