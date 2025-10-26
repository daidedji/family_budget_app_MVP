from django.db import models
from django.contrib.auth.models import User   # for user ownership (Epic 3)

class FamilyMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.role})"


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('IN', 'Money In'),
        ('OUT', 'Money Out'),
    ]

    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.family_member.name} - {self.type} ${self.amount}"


# New model for Epic 3: Expense
class Expense(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # tie to Django user account
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    note = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    recurring = models.BooleanField(default=False)
    recurrence_rule = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} (${self.amount})"
