from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Income, FinancialGoal
# You'll need to create these forms
from .forms import ExpenseForm, IncomeForm, FinancialGoalForm

from django.db.models import Sum
from django.db import models


from sklearn.linear_model import LinearRegression
import numpy as np


@login_required
def dashboard(request):
    user = request.user

    # Fetch latest 5 expenses and incomes.
    expenses = Expense.objects.filter(user=user).order_by('-date')[:5]
    incomes = Income.objects.filter(user=user).order_by('-date')[:5]

    # Calculate total expenses and incomes.
    expenses_sum = Expense.objects.filter(user=user).aggregate(Sum('amount'))[
        'amount__sum'] or 0
    incomes_sum = Income.objects.filter(user=user).aggregate(Sum('amount'))[
        'amount__sum'] or 0

    # Fetch latest 6 months' expenses.
    past_expenses = list(Expense.objects.filter(
        user=user).order_by('-date')[:6])

    # Predict next month's expense using linear regression.
    if len(past_expenses) >= 2:
        X = np.array(range(len(past_expenses))).reshape(-1, 1)
        y = np.array([exp.amount for exp in past_expenses]).reshape(-1, 1)

        model = LinearRegression().fit(X, y)
        next_month_index = len(past_expenses)
        predicted_expense = model.predict(np.array([[next_month_index]]))
    else:
        predicted_expense = [[0]]

    # Aggregate expenses by category.
    category_expenses = Expense.objects.filter(user=user).values(
        'category').annotate(total=Sum('amount'))

    # Build context for the template.
    context = {
        'expenses': expenses,
        'incomes': incomes,
        'goals': FinancialGoal.objects.filter(user=user),
        'expenses_sum': expenses_sum,
        'incomes_sum': incomes_sum,
        'predicted_expense': predicted_expense[0][0],
        'category_expenses': category_expenses
    }

    return render(request, 'dashboard.html', context)


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')

    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form})


@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('dashboard')
    else:
        form = IncomeForm()

    return render(request, 'add_income.html', {'form': form})


@login_required
def add_goal(request):
    if request.method == 'POST':
        form = FinancialGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('dashboard')
    else:
        form = FinancialGoalForm()

    return render(request, 'add_goal.html', {'form': form})

# Continue adding more views as needed.
