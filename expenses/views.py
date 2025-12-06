from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Expense


@login_required
def expense_list(request):
    qs = Expense.objects.order_by('-date')
    total = sum(e.amount for e in qs)
    return render(request, 'expenses/list.html', { 'expenses': qs, 'total': total })

# Create your views here.
