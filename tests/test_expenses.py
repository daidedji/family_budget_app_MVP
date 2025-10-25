import json
from django.urls import reverse

def test_create_expense_requires_amount_and_category(client, django_user_model):
    # arrange: user + login
    user = django_user_model.objects.create_user(username="u1", password="p1")
    client.login(username="u1", password="p1")

    # we will create this URL/view later (TDD: it should fail now = RED)
    url = reverse("expenses-create")
    resp = client.post(
        url,
        data=json.dumps({"amount": "", "category": ""}),
        content_type="application/json",
    )

    # for invalid payloads we expect 400 and field errors
    assert resp.status_code == 400
    data = resp.json()
    assert "amount" in data["errors"]
    assert "category" in data["errors"]


def test_list_expenses_filters_by_month(client, django_user_model):
    from expenses.models import Expense
    import datetime as dt
    from django.urls import reverse

    user = django_user_model.objects.create_user(username="u2", password="p2")
    client.login(username="u2", password="p2")

    # two expenses in different months
    Expense.objects.create(user=user, amount=10, category="Food", date=dt.date(2025, 10, 5))
    Expense.objects.create(user=user, amount=20, category="Rent", date=dt.date(2025, 9, 10))

    url = reverse("expenses-list") + "?month=2025-10"
    resp = client.get(url)
    assert resp.status_code == 200

    items = resp.json()["items"]
    assert any(e["amount"] == 10 for e in items)      # Oct item present
    assert not any(e["amount"] == 20 for e in items)  # Sept item filtered out
