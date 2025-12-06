from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from .models import Visitor


def is_warden(user):
    """Check if the user is a warden (staff)."""
    return user.is_staff


@login_required
def visitor_list(request):
    """Display the list of visitors."""
    if request.user.is_staff:
        # Staff sees all visitors
        qs = Visitor.objects.select_related('student').order_by('-in_time')
    else:
        # Students see only their visitors
        qs = Visitor.objects.filter(student=request.user).order_by('-in_time')

    return render(request, 'visitors/list.html', {'visitors': qs})


@login_required
def apply_visitor(request):
    """Handle visitor application form submission."""
    if request.method == 'POST':
        visitor_name = request.POST.get('visitor_name')
        purpose = request.POST.get('purpose')
        relation = request.POST.get('relation')
        visit_date = request.POST.get('visit_date')
        contact_number = request.POST.get('contact_number')
        
        # Use current time if visit_date is provided
        in_time = timezone.now() if visit_date else None
        # Use relation as id_proof if not provided
        id_proof = relation

        if visitor_name and purpose and relation:
            visitor = Visitor(
                student=request.user,
                visitor_name=visitor_name,
                purpose=purpose,
                in_time=in_time,
                id_proof=id_proof
            )
            visitor.save()
            messages.success(request, 'Visitor application submitted successfully!')
            return redirect('visitors_list')
        else:
            messages.error(request, 'Please fill all required fields.')

    return render(request, 'visitors/apply.html')
