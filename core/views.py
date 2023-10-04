from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Income, FinancialGoal
# You'll need to create these forms
from .forms import ExpenseForm, IncomeForm, FinancialGoalForm

from django.db.models import Sum

from sklearn.linear_model import LinearRegression

import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

from .utils import categorize_uncategorized_expenses, generate_default_forecast

from django.contrib import messages

from django.shortcuts import redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard.html')
    return render(request, 'home.html')
def login_view(request):
    return render(request, 'registration/login.html')
def signup_view(request):
    return render(request, 'registration/signup.html')

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

    # Fetch all expenses for the user.
    allexpenses = Expense.objects.filter(user=user).order_by('date')

    # Convert the expenses to a DataFrame.
    # Create a dataframe with dates for the next 30 days
    user_data = pd.DataFrame(list(allexpenses.values('date', 'amount')))
    user_data.rename(columns={'date': 'ds', 'amount': 'y'}, inplace=True)

    try:
        model = Prophet()
        model.fit(user_data)  # user_data is the actual data for the user
        future = model.make_future_dataframe(periods=7)
        forecast = model.predict(future)
    except (ValueError, Exception):
        # Catch any error related to data issues or Prophet
        forecast = generate_default_forecast()
    # Optionally, inform the user that a default forecast is being shown


    # Extract the predicted value for the next month.
    predicted_expense = forecast['yhat'].iloc[-1]

    # Aggregate expenses by category.
    category_expenses = Expense.objects.filter(user=user).values(
        'category').annotate(total=Sum('amount'))

    # Plot the forecast
    #fig1 = model.plot(forecast)

    # Build context for the template.
    context = {
        'expenses': expenses,
        'incomes': incomes,
        'goals': FinancialGoal.objects.filter(user=user),
        'expenses_sum': expenses_sum,
        'incomes_sum': incomes_sum,
        'category_expenses': category_expenses,
        'predicted_expense': predicted_expense,
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




