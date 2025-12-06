from datetime import date
from django.db.models import Sum, F
from django.shortcuts import render, redirect
from accounts.models import User
from rooms.models import Room
from outpass.models import Outpass
from expenses.models import Expense
from attendance.models import Attendance


def dashboard(request):
    students_count = User.objects.filter(role=User.Roles.STUDENT).count()
    rooms_vacant = Room.objects.filter(status__in=["Vacant", "Partial"]).count()
    rooms_total = Room.objects.count()
    outpass_pending = Outpass.objects.filter(status=Outpass.Status.PENDING).count()
    first_day = date.today().replace(day=1)
    expense_month = Expense.objects.filter(date__gte=first_day).aggregate(total=Sum('amount')).get('total') or 0

    context = {
        'stats': {
            'students': students_count,
            'rooms_total': rooms_total,
            'rooms_vacant': rooms_vacant,
            'outpass_pending': outpass_pending,
            'expense_month': expense_month,
        },
        'recent_outpass': Outpass.objects.order_by('-out_date')[:5],
        'recent_expenses': Expense.objects.order_by('-date')[:5],
    }
    return render(request, 'dashboard.html', context)


def admin_dashboard(request):
    user = request.user
    if not user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('login')
    if not (getattr(user, 'is_staff', False) or getattr(user, 'role', None) in [User.Roles.ADMIN, User.Roles.WARDEN]):
        return render(request, '403.html', status=403)

    students_count = User.objects.filter(role=User.Roles.STUDENT).count()
    rooms_total = Room.objects.count()
    rooms_vacant = Room.objects.filter(status__in=["Vacant", "Partial"]).count()
    outpass_pending = Outpass.objects.filter(status=Outpass.Status.PENDING).count()
    outpass_approved = Outpass.objects.filter(status=Outpass.Status.APPROVED).count()
    first_day = date.today().replace(day=1)
    expense_month = Expense.objects.filter(date__gte=first_day).aggregate(total=Sum('amount')).get('total') or 0

    context = {
        'stats': {
            'students': students_count,
            'rooms_total': rooms_total,
            'rooms_vacant': rooms_vacant,
            'outpass_pending': outpass_pending,
            'outpass_approved': outpass_approved,
            'expense_month': expense_month,
        },
        'recent_outpass': Outpass.objects.order_by('-out_date')[:8],
        'recent_expenses': Expense.objects.order_by('-date')[:8],
    }
    return render(request, 'admin_dashboard.html', context)


def landing(request):
    """Landing route at '/': Show welcome page"""
    return render(request, 'accounts/welcome.html')


def error_403(request, exception=None):
    return render(request, '403.html', status=403)


def error_404(request, exception=None):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)


# Warden pages
def warden_list(request):
    wardens = User.objects.filter(role=User.Roles.WARDEN).order_by('username')
    return render(request, 'warden_list.html', { 'wardens': wardens })


def warden_add(request):
    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        email = (request.POST.get('email') or '').strip()
        password = (request.POST.get('password') or '').strip()
        if username and password:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email or f'{username}@example.com',
                    'role': User.Roles.WARDEN,
                    'is_staff': True,
                }
            )
            if created:
                user.set_password(password)
                user.save()
        return redirect('warden_list')
    return redirect('warden_list')


def warden_dashboard(request):
    students_count = User.objects.filter(role=User.Roles.STUDENT).count()
    rooms_vacant = Room.objects.filter(status__in=["Vacant", "Partial"]).count()
    rooms_total = Room.objects.count()
    outpass_pending = Outpass.objects.filter(status=Outpass.Status.PENDING).count()
    first_day = date.today().replace(day=1)
    expense_month = Expense.objects.filter(date__gte=first_day).aggregate(total=Sum('amount')).get('total') or 0

    context = {
        'stats': {
            'students': students_count,
            'rooms_total': rooms_total,
            'rooms_vacant': rooms_vacant,
            'outpass_pending': outpass_pending,
            'expense_month': expense_month,
        }
    }
    return render(request, 'warden/dashboard.html', context)


def warden_students(request):
    from accounts.forms import UserRegisterForm
    from accounts.models import User as UserModel
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.role = UserModel.Roles.STUDENT
            student.save()
            return redirect('warden_students')
    else:
        form = UserRegisterForm()
    students = UserModel.objects.filter(role=UserModel.Roles.STUDENT).order_by('username')
    return render(request, 'warden/students.html', { 'students': students, 'form': form })


def warden_attendance(request):
    from accounts.models import User as UserModel
    students = UserModel.objects.filter(role=UserModel.Roles.STUDENT).order_by('username')
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        date_str = request.POST.get('date')
        status = request.POST.get('status')
        if student_id and date_str and status:
            from datetime import datetime
            dt = datetime.strptime(date_str, '%Y-%m-%d').date()
            Attendance.objects.update_or_create(
                student_id=student_id,
                date=dt,
                defaults={'status': status}
            )
        return redirect('warden_attendance')
    return render(request, 'warden/attendance.html', { 'students': students })


def warden_outpass(request):
    pending = Outpass.objects.filter(status=Outpass.Status.PENDING).order_by('-out_date')
    return render(request, 'warden/outpass.html', { 'pending': pending })


def warden_approve_outpass(request, pk: int):
    try:
        op = Outpass.objects.get(pk=pk)
        op.status = Outpass.Status.APPROVED
        op.save(update_fields=['status'])
    except Outpass.DoesNotExist:
        pass
    return redirect('warden_outpass')


def warden_visitors(request):
    from visitors.models import Visitor
    visitors = Visitor.objects.all().order_by('-in_time')
    return render(request, 'warden/visitors.html', { 'visitors': visitors })


def warden_approve_visitor(request, pk: int):
    from visitors.models import Visitor
    from django.utils import timezone
    try:
        vs = Visitor.objects.get(pk=pk)
        if not vs.out_time:
            vs.out_time = timezone.now()
            vs.save(update_fields=['out_time'])
    except Visitor.DoesNotExist:
        pass
    return redirect('warden_visitors')


def warden_expenses(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        item = request.POST.get('item')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        if date and item and amount and category:
            Expense.objects.create(date=date, item=item, amount=amount, category=category)
        return redirect('warden_expenses')
    latest = Expense.objects.order_by('-date')[:10]
    return render(request, 'warden/expenses.html', { 'latest': latest })


# Student pages
def student_dashboard(request):
    return render(request, 'student/dashboard.html')