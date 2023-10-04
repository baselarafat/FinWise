from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
urlpatterns = [
    #path('', views.dashboard, name='root'),  # set dashboard as the root URL
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-income/', views.add_income, name='add_income'),
    path('add-goal/', views.add_goal, name='add_goal'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', CreateView.as_view(
        template_name='registration/signup.html',
        form_class=UserCreationForm,
        success_url=reverse_lazy('login')
    ), name='signup'),

    # ... other URL patterns ...
]