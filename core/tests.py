from django.test import TestCase
from django.urls import reverse
from core.forms import ExpenseForm, IncomeForm, FinancialGoalForm
from core.models import Expense, Income, FinancialGoal, User

# Test Views
class ViewTests(TestCase):
    
    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # 302 is the status code for redirection

    def test_add_expense_view_status_code(self):
        response = self.client.get(reverse('add_expense'))
        self.assertEqual(response.status_code, 302)

    def test_add_income_view_status_code(self):
        response = self.client.get(reverse('add_income'))
        self.assertEqual(response.status_code, 302)  

    def test_add_goal_view_status_code(self):
        response = self.client.get(reverse('add_goal'))
        self.assertEqual(response.status_code, 302)

# Test User Model
class UserModelTests(TestCase):
    def test_user_creation(self):
        user = User.objects.create(username="testuser", password="testpassword")
        self.assertIsInstance(user, User)

# Test Form Validity
class ExpenseFormTest(TestCase):
    def test_valid_form(self):
        data = {'description': 'Test Expense', 'category': 'groceries', 'amount': 100.50}
        form = ExpenseForm(data=data)
        self.assertTrue(form.is_valid())

class IncomeFormTest(TestCase):
    def test_valid_form(self):
        data = {'description': 'Test Income', 'amount': 200.50}
        form = IncomeForm(data=data)
        self.assertTrue(form.is_valid())

class FinancialGoalFormTest(TestCase):
    def test_valid_form(self):
        data = {'description': 'Test Goal', 'target_amount': 5000, 'target_date': '2023-12-31'}
        form = FinancialGoalForm(data=data)
        self.assertTrue(form.is_valid())

# Test Model Creation 
class ModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_expense_creation(self):
        expense = Expense.objects.create(description="Test Expense", category="groceries", amount=100.50, user=self.user)
        self.assertIsInstance(expense, Expense)

    def test_income_creation(self):
        income = Income.objects.create(description="Test Income", amount=200.50, user=self.user)
        self.assertIsInstance(income, Income)

    def test_goal_creation(self):
        goal = FinancialGoal.objects.create(description="Test Goal", target_amount=5000, target_date='2023-12-31', user=self.user)
        self.assertIsInstance(goal, FinancialGoal)
