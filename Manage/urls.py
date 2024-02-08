from django.urls import path,include
from .views import get_object_counts,add_semester,get_semesters
urlpatterns = [        
    path('get_object_counts',get_object_counts,name='get_object_counts'),    
    path('add_semester/',add_semester,name='add_semester'),
    path('get_semesters/',get_semesters,name='get_semesters'),
]
