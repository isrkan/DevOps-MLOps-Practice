from django.shortcuts import render, redirect, get_object_or_404
from expenses.models import Expense

# Create your views here.
def home(request):
    return render(request, 'expenses/home.html')

def expenses_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expenses/expenses_list.html', {'expenses': expenses})

def approve_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.approved = not expense.approved
        expense.save()
        return redirect('expenses_list')
    return render(request, 'expenses/approve_expense.html', {'expense': expense})
