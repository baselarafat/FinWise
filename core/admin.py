from django.contrib import admin
from .models import Expense, Income, FinancialGoal,Category

admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(FinancialGoal)
admin.site.register(Category)