from django.db import models

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
