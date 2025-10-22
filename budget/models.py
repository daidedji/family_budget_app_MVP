from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100)
    visibility = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Funds(models.Model):
    total = models.FloatField(default=0.0)

    def __str__(self):
        return f"Funds: ${self.total:.2f}"


class Debt(models.Model):
    total_debt = models.FloatField(default=0.0)

    def __str__(self):
        return f"Debt: ${self.total_debt:.2f}"


class Transaction(models.Model):
    TRANSACTION_TYPES = [('IN', 'Money In'), ('OUT', 'Money Out')]
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    amount = models.FloatField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.get_type_display()} - ${self.amount:.2f}"


class Budget(models.Model):
    needs = models.FloatField(default=0.0)
    wants = models.FloatField(default=0.0)
    savings = models.FloatField(default=0.0)

    def __str__(self):
        return f"Budget (50/30/20)"


class FamilyRelation(models.Model):
    user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    relative = models.ForeignKey(User, related_name='relative', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} ↔ {self.relative.name}"


class Bill(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    due_date = models.DateField()
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - ${self.amount}"
