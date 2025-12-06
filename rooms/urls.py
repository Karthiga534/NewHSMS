from django.urls import path
from .views import room_list, add_room


urlpatterns = [
    path('', room_list, name='rooms_list'),
    path('add/', add_room, name='rooms_add'),
]

