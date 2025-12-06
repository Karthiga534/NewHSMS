from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import Outpass


def is_warden(user):
    return user.is_staff and not user.is_superuser

@login_required
def outpass_list(request):
    if is_warden(request.user):
        # Wardens see all outpasses separated by status
        pending = Outpass.objects.filter(status=Outpass.Status.PENDING).select_related('student').order_by('-out_date')
        approved = Outpass.objects.filter(status=Outpass.Status.APPROVED).select_related('student').order_by('-out_date')
        rejected = Outpass.objects.filter(status=Outpass.Status.REJECTED).select_related('student').order_by('-out_date')
        context = {
            'pending': pending,
            'approved': approved,
            'rejected': rejected
        }
        return render(request, 'warden/outpass.html', context)
    else:
        # Students see only their outpasses
        qs = Outpass.objects.filter(student=request.user).order_by('-out_date')
        return render(request, 'outpass/list.html', {'outpasses': qs})

@login_required
def apply_outpass(request):
    if request.method == 'POST':
        # Process the form submission
        reason = request.POST.get('reason')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        destination = request.POST.get('destination')
        contact_number = request.POST.get('contact_number')
        parent_consent = request.POST.get('parent_consent') == 'on'
        
        # Convert dates to datetime objects
        from_datetime = datetime.strptime(from_date, '%Y-%m-%d')
        to_datetime = datetime.strptime(to_date, '%Y-%m-%d')
        
        # Create new outpass
        outpass = Outpass(
            student=request.user,
            reason=reason,
            out_date=from_datetime,
            expected_return=to_datetime,
            status=Outpass.Status.PENDING
        )
        # Store additional info in the reason field if needed
        if destination or contact_number:
            outpass.reason = f"{reason} - Destination: {destination}, Contact: {contact_number}"
        outpass.save()
        
        messages.success(request, 'Your outpass application has been submitted successfully!')
        return redirect('outpass_list')
    return render(request, 'outpass/apply.html')

@login_required
@user_passes_test(is_warden)
def approve_outpass(request, pk):
    outpass = get_object_or_404(Outpass, pk=pk)
    outpass.status = Outpass.Status.APPROVED
    outpass.approved_at = timezone.now()
    if request.method == 'POST':
        outpass.warden_remarks = request.POST.get('remarks', '')
    outpass.save()
    messages.success(request, f'Outpass #{pk} has been approved')
    return redirect('outpass_list')

@login_required
@user_passes_test(is_warden)
def reject_outpass(request, pk):
    outpass = get_object_or_404(Outpass, pk=pk)
    outpass.status = Outpass.Status.REJECTED
    outpass.rejected_at = timezone.now()
    if request.method == 'POST':
        outpass.warden_remarks = request.POST.get('remarks', '')
    outpass.save()
    messages.success(request, f'Outpass #{pk} has been rejected')
    return redirect('outpass_list')
