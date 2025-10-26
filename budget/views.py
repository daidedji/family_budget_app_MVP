from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Expense
import json
from datetime import date

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
