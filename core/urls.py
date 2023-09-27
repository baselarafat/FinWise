from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='root'),  # set dashboard as the root URL
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-income/', views.add_income, name='add_income'),
    path('add-goal/', views.add_goal, name='add_goal'),


    # ... other URL patterns ...
]
