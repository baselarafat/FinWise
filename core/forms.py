from django import forms
from .models import Expense, Income, FinancialGoal


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'category', 'amount']
        # User field is excluded because it's assigned in the view


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['description', 'amount']


class FinancialGoalForm(forms.ModelForm):
    class Meta:
        model = FinancialGoal
        fields = ['description', 'target_amount', 'target_date']
