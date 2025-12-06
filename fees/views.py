from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import datetime
from .models import Fee


def is_warden(user):
    return user.is_staff and not user.is_superuser


@login_required
def fee_list(request):
    if is_warden(request.user):
        qs = Fee.objects.select_related('student').order_by('due_date')
    else:
        qs = Fee.objects.filter(student=request.user).order_by('due_date')
    return render(request, 'fees/list.html', {'fees': qs})


@login_required
def apply_fee(request):
    if request.method == 'POST':
        fee_type = request.POST.get('fee_type')
        amount = request.POST.get('amount')
        payment_date = request.POST.get('payment_date')
        payment_method = request.POST.get('payment_method')
        reference_number = request.POST.get('reference_number', '')
        
        if fee_type and amount and payment_date and payment_method:
            try:
                amount_decimal = float(amount)
                payment_date_obj = datetime.strptime(payment_date, '%Y-%m-%d').date()
                
                # Create fee application
                fee = Fee(
                    student=request.user,
                    total_amount=amount_decimal,
                    paid_amount=0,  # Start with 0 paid amount until approved
                    due_date=payment_date_obj,
                    status=Fee.Status.UNPAID  # Will be updated by warden
                )
                fee.save()
                
                messages.success(request, 'Fee application submitted successfully!')
                return redirect('fees_list')
            except ValueError as e:
                messages.error(request, f'Invalid amount or date format: {str(e)}')
        else:
            messages.error(request, 'Please fill all required fields.')
    
    return render(request, 'fees/apply.html')


@login_required
@user_passes_test(is_warden)
def approve_fee(request, pk):
    fee = Fee.objects.get(pk=pk)
    fee.status = Fee.Status.PAID
    fee.save()
    messages.success(request, f'Fee #{pk} has been approved')
    return redirect('fees_list')
