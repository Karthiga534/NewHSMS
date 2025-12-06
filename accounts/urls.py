from django.urls import path
from .views import UserLoginView, UserLogoutView, custom_logout, register, profile


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
]

