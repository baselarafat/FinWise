from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Income, FinancialGoal
# You'll need to create these forms
from .forms import ExpenseForm, IncomeForm, FinancialGoalForm

from django.db.models import Sum


@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user).order_by(
        '-date')[:5]  # Get last 5 expenses
    incomes = Income.objects.filter(user=request.user).order_by(
        '-date')[:5]  # Get last 5 incomes
    goals = FinancialGoal.objects.filter(user=request.user)
    expenses_sum = Expense.objects.filter(
        user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    incomes_sum = Income.objects.filter(user=request.user).aggregate(
        Sum('amount'))['amount__sum'] or 0

    context = {
        'expenses': expenses,
        'incomes': incomes,
        'goals': goals,
        'expenses_sum': expenses_sum,
        'incomes_sum': incomes_sum,
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
