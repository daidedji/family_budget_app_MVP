from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Expense
import json
from datetime import date, datetime

@csrf_exempt
@login_required
def create_expense(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=405)

    data = json.loads(request.body) if request.content_type == "application/json" else request.POST
    try:
        amount = float(data.get("amount", 0))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Amount must be a number"}, status=400)

    category = (data.get("category") or "").strip()
    note = data.get("note", "")

    if amount <= 0 or not category:
        return JsonResponse({"error": "Invalid input"}, status=400)

    Expense.objects.create(
        user=request.user,
        amount=amount,
        category=category,
        note=note,
        date=date.today(),
    )
    return JsonResponse({"message": "Expense created"}, status=201)


@login_required
def list_expenses(request):
    month_str = request.GET.get("month")
    if not month_str:
        return JsonResponse({"error": "Month parameter is required"}, status=400)

    try:
        year, month = map(int, month_str.split("-"))
        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date()
        else:
            end_date = datetime(year, month + 1, 1).date()
    except Exception:
        return JsonResponse({"error": "Invalid month format (use YYYY-MM)"}, status=400)

    expenses = Expense.objects.filter(
        user=request.user, date__gte=start_date, date__lt=end_date
    ).values("id", "amount", "category", "note", "date")

    return JsonResponse(list(expenses), safe=False, status=200)
