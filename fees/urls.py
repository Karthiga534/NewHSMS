from django.urls import path
from .views import fee_list, apply_fee, approve_fee


urlpatterns = [
    path('', fee_list, name='fees_list'),
    path('apply/', apply_fee, name='apply_fee'),
    path('approve/<int:pk>/', approve_fee, name='approve_fee'),
]

