from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class Expense(models.Model):
    SOURCE_CHOICES = [
        ('manual', 'Manual Entry'),
        ('voice_input', 'Voice Input'),
        ('receipt_scan', 'Receipt Scan'),
        ('api', 'API'),
    ]
    
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=266)
    created_from = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='manual')

    def __str__(self):
        return self.category

    class Meta:
        ordering: ['-date']


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class ExpenseLimit(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    daily_expense_limit=models.IntegerField()
