from django.urls import path
from . import views

urlpatterns = [
    path("expenses", views.create_expense, name="expenses-create"),
]
