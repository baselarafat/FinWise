from django.urls import path
from . import views

urlpatterns = [
    #path('', views.dashboard, name='root'),  # set dashboard as the root URL
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-income/', views.add_income, name='add_income'),
    path('add-goal/', views.add_goal, name='add_goal'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),


    # ... other URL patterns ...
]
