from django.urls import path
from .views import visitor_list, apply_visitor


urlpatterns = [
    path('', visitor_list, name='visitors_list'),
    path('apply/', apply_visitor, name='apply_visitor'),
]

