from django.db import models
from django.utils import timezone

class Income(models.Model):
    source = models.CharField(max_length=100)
    amount = models.FloatField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.source} - ${self.amount:.2f}"


class Expense(models.Model):
    category = models.CharField(max_length=100)   # ← this field was missing
    amount = models.FloatField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.category} - ${self.amount:.2f}"
