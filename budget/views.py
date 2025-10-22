from django.shortcuts import render, redirect
from .models import User, Funds, Debt, Transaction, Budget, Bill
from .forms import TransactionForm, DebtForm, BillForm, UserForm

def index(request):
    funds, _ = Funds.objects.get_or_create(id=1)
    debt, _ = Debt.objects.get_or_create(id=1)
    budget, _ = Budget.objects.get_or_create(id=1)

    # Calculate 50/30/20
    budget.needs = funds.total * 0.5
    budget.wants = funds.total * 0.3
    budget.savings = funds.total * 0.2
    budget.save()

    chat_output = ""

    # Handle POST requests
    if request.method == 'POST':
        if 'transaction_submit' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                t = form.save()
                if t.type == 'IN':
                    funds.total += t.amount
                else:
                    funds.total -= t.amount
                funds.save()
                return redirect('index')

        elif 'debt_submit' in request.POST:
            dform = DebtForm(request.POST, instance=debt)
            if dform.is_valid():
                dform.save()
                return redirect('index')

        elif 'bill_submit' in request.POST:
            bform = BillForm(request.POST)
            if bform.is_valid():
                bform.save()
                return redirect('index')

        elif 'user_submit' in request.POST:
            uform = UserForm(request.POST)
            if uform.is_valid():
                uform.save()
                return redirect('index')

        elif 'chat_submit' in request.POST:
            chat_input = request.POST.get('chat_input', '')
            chat_output = f"You said: '{chat_input}'. AI CHAT BOT WORK IN PROGRESS IF IT TAKES TOO LONG MAY CUT :/"

    context = {
        'funds': funds,
        'debt': debt,
        'budget': budget,
        'transactions': Transaction.objects.all().order_by('-date'),
        'bills': Bill.objects.all().order_by('due_date'),
        'users': User.objects.all(),
        'form': TransactionForm(),
        'dform': DebtForm(instance=debt),
        'bform': BillForm(),
        'uform': UserForm(),
        'chat_output': chat_output,
    }

    return render(request, 'index.html', context)
