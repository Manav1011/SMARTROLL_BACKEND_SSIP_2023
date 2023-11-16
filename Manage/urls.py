from django.urls import path
from .views import get_batches,add_batches,get_semesters
urlpatterns = [
    path('get_batches',get_batches,name='get_batches'),
    path('add_batches',add_batches,name='add_batches'),
    path('get_semesters',get_semesters,name='get_semesters'),
]
