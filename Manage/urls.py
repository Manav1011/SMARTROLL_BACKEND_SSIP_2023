from django.urls import path
from .views import get_batches,add_batches,get_semesters,add_semester
urlpatterns = [
    path('get_batches',get_batches,name='get_batches'),
    path('add_batch',add_batches,name='add_batch'),
    path('get_semesters',get_semesters,name='get_semesters'),
    path('add_semester',add_semester,name='add_semester'),
]
