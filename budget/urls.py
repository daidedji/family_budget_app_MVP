from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('income/', views.add_income_view, name='add_income'),
    path('expense/', views.add_expense_view, name='add_expense'),
    path('summary/', views.summary_view, name='summary'),
]
