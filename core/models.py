from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):
    CATEGORIES = [
        ('groceries', 'Groceries'),
        ('entertainment', 'Entertainment'),
        ('bills', 'Bills'),
        # ... add more as needed
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORIES, max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description


class FinancialGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    target_date = models.DateField()

    def __str__(self):
        return self.description
