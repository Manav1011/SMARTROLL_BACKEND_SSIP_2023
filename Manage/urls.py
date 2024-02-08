from django.urls import path,include
from .views import get_object_counts,add_semester,get_semesters,add_division,get_subjects,add_subject
urlpatterns = [        
    path('get_object_counts',get_object_counts,name='get_object_counts'),    
    path('add_semester/',add_semester,name='add_semester'),
    path('get_semesters/',get_semesters,name='get_semesters'),
    path('add_division/',add_division,name='add_division'),
    path('get_subjects/',get_subjects,name='get_subjects'),
    path('add_subject/',add_subject,name='add_subject'),
]
