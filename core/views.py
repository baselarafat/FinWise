from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Income, FinancialGoal
# You'll need to create these forms
from .forms import ExpenseForm, IncomeForm, FinancialGoalForm

from django.db.models import Sum

import pandas as pd
from prophet import Prophet

from .utils import categorize_uncategorized_expenses, generate_default_forecast

from django.contrib import messages

from django.shortcuts import redirect , get_object_or_404

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard.html')
    return render(request, 'home.html')
def login_view(request):
    return render(request, 'registration/login.html')
def signup_view(request):
    return render(request, 'registration/signup.html')

# A simplified dashboard without analysis 
@login_required
def dashboard(request):
    user = request.user

    # Fetch latest 5 expenses and incomes.
    expenses = Expense.objects.filter(user=user).order_by('-date')[:5]
    incomes = Income.objects.filter(user=user).order_by('-date')[:5]

    # Calculate total expenses and incomes.
    expenses_sum = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    incomes_sum = Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0

    # Aggregate expenses by category.
    category_expenses = Expense.objects.filter(user=user).values('category').annotate(total=Sum('amount'))

    # Build context for the template.
    context = {
        'expenses': expenses,
        'incomes': incomes,
        'goals': FinancialGoal.objects.filter(user=user),
        'expenses_sum': expenses_sum,
        'incomes_sum': incomes_sum,
        'category_expenses': category_expenses,
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
            messages.success(request, "Expense added successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "There was an error adding the expense.")
    else:
        form = ExpenseForm()

    categorize_uncategorized_expenses()
    return render(request, 'add_expense.html', {'form': form})


@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, "Income added successfully!")
            return redirect('dashboard')
        else: 
            messages.error(request, "There was an error adding the income.")
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
            messages.success(request, "Goal added successfully!")
            return redirect('dashboard')
        else: 
            messages.error(request, "There was an error adding the goal.")
    else:
        form = FinancialGoalForm()

    return render(request, 'add_goal.html', {'form': form})

@login_required
def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "There was an error updating the expense.")
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'update_expense.html', {'form': form})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted successfully!")
        return redirect('dashboard')
    return render(request, 'delete_expense.html', {'expense': expense})

@login_required
def update_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, "Income updated successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "There was an error updating the income.")
    else:
        form = IncomeForm(instance=income)
    return render(request, 'update_income.html', {'form': form})

@login_required
def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    if request.method == 'POST':
        income.delete()
        messages.success(request, "Income deleted successfully!")
        return redirect('dashboard')
    return render(request, 'delete_income.html', {'income': income})

@login_required
def update_goal(request, goal_id):
    goal = get_object_or_404(FinancialGoal, id=goal_id, user=request.user)
    if request.method == 'POST':
        form = FinancialGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, "Goal updated successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "There was an error updating the goal.")
    else:
        form = FinancialGoalForm(instance=goal)
    return render(request, 'update_goal.html', {'form': form})

@login_required
def delete_goal(request, goal_id):
    goal = get_object_or_404(FinancialGoal, id=goal_id, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, "Goal deleted successfully!")
        return redirect('dashboard')
    return render(request, 'delete_goal.html', {'goal': goal})

@login_required
def visualize_finances(request):
    user = request.user
    expenses = Expense.objects.filter(user=user).order_by('date')
    incomes = Income.objects.filter(user=user).order_by('date')

    # Convert to lists for plotting
    expense_dates = [e.date for e in expenses]
    expense_amounts = [e.amount for e in expenses]
    income_dates = [i.date for i in incomes]
    income_amounts = [i.amount for i in incomes]

    context = {
        'expense_dates': expense_dates,
        'expense_amounts': expense_amounts,
        'income_dates': income_dates,
        'income_amounts': income_amounts
    }
    return render(request, 'visualize_finances.html', context)

@login_required
def compare_forecast(request):
    user = request.user
    expenses = Expense.objects.filter(user=user).order_by('date')

    # Convert to DataFrame
    user_data = pd.DataFrame(list(expenses.values('date', 'amount')))
    user_data.rename(columns={'date': 'ds', 'amount': 'y'}, inplace=True)

    model = Prophet()
    model.fit(user_data)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Extract actual and predicted values
    actual_expenses = user_data['y'].tolist()
    predicted_expenses = forecast['yhat'].tolist()

    context = {
        'actual_expenses': actual_expenses,
        'predicted_expenses': predicted_expenses
    }
    return render(request, 'compare_forecast.html', context)

@login_required
def savings_suggestions(request):
    user = request.user
    expenses = Expense.objects.filter(user=user).order_by('date')
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Simple logic: If the user's expenses are more than a certain threshold, suggest savings
    suggestions = []
    if total_expense > 1000:  # You can adjust this threshold
        suggestions.append("Consider cutting down on dining out.")
        suggestions.append("Review your monthly subscriptions.")
        # ... add more suggestions

    context = {
        'suggestions': suggestions
    }
    return render(request, 'savings_suggestions.html', context)



