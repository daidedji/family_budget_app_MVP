from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('expenses', views.create_expense, name='create_expense'),
    path('expenses/list', views.list_expenses, name='list_expenses'),
]
