from django import forms
from .models import Expense, Income, FinancialGoal, Category


class ExpenseForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'category', 'notes', 'tags']
        # User field is excluded because it's assigned in the view


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['description', 'amount']


class FinancialGoalForm(forms.ModelForm):
    class Meta:
        model = FinancialGoal
        fields = ['description', 'target_amount', 'target_date']
