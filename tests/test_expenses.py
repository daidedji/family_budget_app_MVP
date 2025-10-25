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
