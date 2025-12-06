from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Student


@login_required
def student_list(request):
    students = Student.objects.select_related('user').all().order_by('reg_no')
    return render(request, 'students/list.html', { 'students': students })

# Create your views here.
