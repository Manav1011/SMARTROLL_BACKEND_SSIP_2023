from django.urls import path,include
from .views import get_object_counts,add_semester,get_semesters,add_division,add_batch,get_batches,get_divisions
urlpatterns = [        
    path('get_object_counts',get_object_counts,name='get_object_counts'),    
    path('add_semester/',add_semester,name='add_semester'),
    path('get_semesters',get_semesters,name='get_semesters'),
    path('add_division/',add_division,name='add_division'),
    path('add_batch/',add_batch,name='add_batch'),
    path('get_batches',get_batches,name='get_batches'),
    path('get_divisions',get_divisions,name='get_divisions'),
]
