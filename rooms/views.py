from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import F
from .models import Room


@login_required
def room_list(request):
    qs = Room.objects.all().order_by('room_no')
    if request.GET.get('available'):
        qs = qs.filter(occupied_count__lt=F('capacity'))
    rooms = qs
    return render(request, 'rooms/list.html', { 'rooms': rooms })


@login_required
@require_http_methods(["POST"])
def add_room(request):
    room_no = (request.POST.get('room_no') or '').strip()
    capacity = int(request.POST.get('capacity') or 0)
    occupied = int(request.POST.get('occupied_count') or 0)

    if not room_no or capacity < 1 or occupied < 0 or occupied > capacity:
        return redirect('/rooms/?available=1')

    status = 'Vacant'
    if occupied == 0:
        status = 'Vacant'
    elif occupied >= capacity:
        status = 'Occupied'
    else:
        status = 'Partial'

    Room.objects.get_or_create(
        room_no=room_no,
        defaults={
            'capacity': capacity,
            'occupied_count': occupied,
            'status': status,
        }
    )
    return redirect('/rooms/?available=1')

# Create your views here.
