from django.conf import settings
from django.db import models
from django.utils import timezone

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    note = models.CharField(max_length=255, blank=True)
    date = models.DateField(default=timezone.now)
    is_recurring = models.BooleanField(default=False)
    recurrence_rule = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user} • {self.category} • {self.amount}"
    


# Create your models here.
