from django.shortcuts import render, redirect
from .models import Income, Expense

# Simulated login (stores name in session)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        if username:
            request.session['username'] = username
            return redirect('dashboard')
    return render(request, "login.html")

def dashboard_view(request):
    username = request.session.get('username', None)
    if not username:
        return redirect('login')

    total_income = sum(i.amount for i in Income.objects.all())
    total_expense = sum(e.amount for e in Expense.objects.all())
    balance = total_income - total_expense

    context = {
        "username": username,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
    }
    return render(request, "dashboard.html", context)

def add_income_view(request):
    username = request.session.get('username', None)
    if not username:
        return redirect('login')

    if request.method == "POST":
        source = request.POST.get("source")
        amount = request.POST.get("amount")
        if source and amount:
            Income.objects.create(source=source, amount=float(amount))
            return redirect('dashboard')

    return render(request, "add_income.html", {"username": username})

def add_expense_view(request):
    username = request.session.get('username', None)
    if not username:
        return redirect('login')

    if request.method == "POST":
        category = request.POST.get("category")
        amount = request.POST.get("amount")
        if category and amount:
            Expense.objects.create(category=category, amount=float(amount))
            return redirect('dashboard')

    return render(request, "add_expense.html", {"username": username})

def summary_view(request):
    username = request.session.get('username', None)
    if not username:
        return redirect('login')

    incomes = Income.objects.all()
    expenses = Expense.objects.all()
    total_income = sum(i.amount for i in incomes)
    total_expense = sum(e.amount for e in expenses)
    balance = total_income - total_expense

    context = {
        "username": username,
        "incomes": incomes,
        "expenses": expenses,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
    }
    return render(request, "summary.html", context)
