from django.shortcuts import render, redirect, get_object_or_404
from expenses.models import Expense
from prometheus_client import Histogram
from django.http import HttpResponse

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

# Create a Histogram to track request processing time
request_processing_time = Histogram('request_processing_seconds', 'Time spent processing a request')

@request_processing_time.time()  # This decorator measures the time spent in this view
def my_view(request):
   # Simulate request processing
   return HttpResponse("Request processed.")