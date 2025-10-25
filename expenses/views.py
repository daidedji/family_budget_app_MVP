from django.shortcuts import render
import json
import datetime as dt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Expense

@login_required
def create_expense(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"errors": {"body": "Invalid JSON"}}, status=400)

    errors = {}
    amount = data.get("amount")
    category = (data.get("category") or "").strip()

    # validation required by test
    try:
        amount_val = float(amount)
        if amount_val <= 0:
            errors["amount"] = "Amount must be greater than 0."
    except Exception:
        errors["amount"] = "Amount must be a number."

    if not category:
        errors["category"] = "Category is required."

    if errors:
        return JsonResponse({"errors": errors}, status=400)

    expense = Expense.objects.create(
        user=request.user,
        amount=amount_val,
        category=category,
        note=(data.get("note") or ""),
        date=dt.date.today()
    )

    return JsonResponse(
        {"id": expense.id, "amount": float(expense.amount), "category": expense.category, "date": str(expense.date)},
        status=201,
    )
def list_expenses(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    month = request.GET.get("month")  # expected YYYY-MM
    qs = Expense.objects.filter(user=request.user)

    if month:
        try:
            year_str, mon_str = month.split("-")
            year, mon = int(year_str), int(mon_str)
            import calendar, datetime as dt
            first = dt.date(year, mon, 1)
            last = dt.date(year, mon, calendar.monthrange(year, mon)[1])
            qs = qs.filter(date__gte=first, date__lte=last)
        except Exception:
            return JsonResponse({"errors": {"month": "Invalid month format (YYYY-MM)"}}, status=400)

    items = [
        {"id": e.id, "amount": float(e.amount), "category": e.category, "date": str(e.date)}
        for e in qs.order_by("-date", "-id")
    ]
    return JsonResponse({"items": items}, status=200)
# Create your views here.
