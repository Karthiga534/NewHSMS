from django.db import models


class Expense(models.Model):
    class Category(models.TextChoices):
        FOOD = "Food", "Food"
        WATER = "Water", "Water"
        GAS = "Gas", "Gas"
        OTHERS = "Others", "Others"

    date = models.DateField()
    item = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=Category.choices)

    def __str__(self) -> str:
        return f"{self.date} - {self.item} - {self.amount}"

# Create your models here.
