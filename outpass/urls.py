from django.urls import path
from .views import outpass_list, apply_outpass, approve_outpass, reject_outpass


urlpatterns = [
    path('', outpass_list, name='outpass_list'),
    path('apply/', apply_outpass, name='apply_outpass'),
    path('approve/<int:pk>/', approve_outpass, name='approve_outpass'),
    path('reject/<int:pk>/', reject_outpass, name='reject_outpass'),
]

