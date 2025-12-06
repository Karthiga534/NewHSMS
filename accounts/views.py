from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import UserRegisterForm, UserUpdateForm, CustomLoginForm
from django.urls import reverse
from .models import User



class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        # If already logged in, honor ?next= then role-based redirect
        if request.user.is_authenticated:
            redirect_to = self.get_redirect_url()
            if redirect_to:
                return redirect(redirect_to)
            return self.redirect_by_role(request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Use built-in login then redirect via get_success_url."""
        user = form.get_user()
        selected_role = form.cleaned_data.get('role')
        if user is None:
            messages.error(self.request, 'Invalid username or password.')
            return self.form_invalid(form)
        # For non-staff users, ensure selected role matches
        if not (user.is_superuser or user.is_staff) and str(user.role) != str(selected_role):
            messages.error(self.request, f'Invalid role selection. Your account is registered as {user.get_role_display()}.')
            return self.form_invalid(form)
        messages.success(self.request, f'Welcome back, {user.username}!')
        login(self.request, user)
        return self.redirect_by_role(user)

    def redirect_by_role(self, user):
        """Centralized role-based redirect."""
        if getattr(user, 'role', None) == user.Roles.WARDEN and not user.is_superuser:
            return redirect('warden_dashboard')
        if getattr(user, 'role', None) == user.Roles.ADMIN or user.is_superuser:
            return redirect('admin_dashboard')
        if getattr(user, 'role', None) == user.Roles.STUDENT:
            return redirect('student_dashboard')
        return redirect('home')

    def get_success_url(self):
        """This is called by LoginView after form_valid."""
        # 1) Honor ?next= if present and allowed
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to
        # 2) Otherwise, route by role
        user = self.request.user
        if getattr(user, 'role', None) == user.Roles.WARDEN and not user.is_superuser:
            return reverse('warden_dashboard')
        if getattr(user, 'role', None) == user.Roles.STUDENT:
            return reverse('student_dashboard')
        if getattr(user, 'role', None) == user.Roles.ADMIN or user.is_superuser:
            return reverse('admin_dashboard')
        return reverse('home')


class UserLogoutView(LogoutView):
    next_page = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        # Allow both GET and POST requests for logout
        if request.method == 'GET':
            # For GET requests, redirect to logout with POST method
            return self.post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


@require_http_methods(["GET", "POST"])
def custom_logout(request):
    """Custom logout view that handles both GET and POST requests"""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        user = request.user
        is_admin_or_warden = (
            user.is_superuser or user.is_staff or getattr(user, 'role', None) in [User.Roles.ADMIN, User.Roles.WARDEN]
        )
        if not is_admin_or_warden:
            return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', { 'form': form })


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', { 'form': form })

# Create your views here.
