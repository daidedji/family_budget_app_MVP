
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Expense
from datetime import date

class ExpenseModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")

    def test_create_expense_model_fields(self):
        """Expense model should correctly save basic fields."""
        exp = Expense.objects.create(
            user=self.user,
            amount=100.50,
            category="Food",
            note="Groceries",
            date=date.today(),
            recurring=False
        )
        self.assertEqual(exp.amount, 100.50)
        self.assertEqual(exp.category, "Food")
        self.assertFalse(exp.recurring)

class ExpenseAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apitester", password="pass123")
        self.client.login(username="apitester", password="pass123")
        self.create_url = reverse("create_expense")

    def test_post_valid_expense_creates_record(self):
        data = {"amount": 25, "category": "Transport", "note": "Bus fare"}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Expense.objects.first().category, "Transport")

    def test_post_invalid_expense_fails(self):
        data = {"amount": -10, "category": ""}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 400)

class ExpenseListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="listuser", password="pass123")
        self.client.login(username="listuser", password="pass123")
        self.list_url = reverse("list_expenses")

    def test_get_monthly_expenses_returns_correct_records(self):
        """Should return expenses only for the selected month."""
        Expense.objects.create(
            user=self.user, amount=50, category="Food", date=date(2025, 10, 1)
        )
        Expense.objects.create(
            user=self.user, amount=100, category="Transport", date=date(2025, 9, 30)
        )
        response = self.client.get(self.list_url, {"month": "2025-10"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["category"], "Food")

    def test_get_expenses_requires_login(self):
        """Unauthenticated users should get 403."""
        self.client.logout()
        response = self.client.get(self.list_url, {"month": "2025-10"})
        self.assertEqual(response.status_code, 403)
