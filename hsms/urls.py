"""
URL configuration for hsms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import (
    dashboard, admin_dashboard, landing,
    warden_list, warden_add,
    warden_dashboard, warden_students, warden_attendance,
    warden_outpass, warden_approve_outpass,
    warden_visitors, warden_approve_visitor,
    warden_expenses, student_dashboard,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('rooms/', include('rooms.urls')),
    path('outpass/', include('outpass.urls')),
    path('expenses/', include('expenses.urls')),
    path('visitors/', include('visitors.urls')),
    path('fees/', include('fees.urls')),
    path('admin-dashboard/', login_required(admin_dashboard), name='admin_dashboard'),
    path('warden/', login_required(warden_list), name='warden_list'),
    path('warden/add/', login_required(warden_add), name='warden_add'),
    # Warden panel
    path('warden/dashboard/', login_required(warden_dashboard), name='warden_dashboard'),
    path('warden/students/', login_required(warden_students), name='warden_students'),
    path('warden/attendance/', login_required(warden_attendance), name='warden_attendance'),
    path('warden/outpass/', login_required(warden_outpass), name='warden_outpass'),
    path('warden/outpass/approve/<int:pk>/', login_required(warden_approve_outpass), name='warden_approve_outpass'),
    path('warden/visitors/', login_required(warden_visitors), name='warden_visitors'),
    path('warden/visitors/approve/<int:pk>/', login_required(warden_approve_visitor), name='warden_approve_visitor'),
    path('warden/expenses/', login_required(warden_expenses), name='warden_expenses'),
    # Student
    path('student/dashboard/', login_required(student_dashboard), name='student_dashboard'),
    path('', landing, name='landing'),
    path('dashboard/', login_required(dashboard), name='home'),
]

# Error handlers
handler403 = 'hsms.views.error_403'
handler404 = 'hsms.views.error_404'
handler500 = 'hsms.views.error_500'
