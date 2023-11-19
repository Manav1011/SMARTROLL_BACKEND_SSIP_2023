from django.urls import path
from .views import get_batches,add_batches,get_semesters,add_semester,get_subjects,add_subjects,get_teachers,add_teacher,add_subjects_to_teacher,get_object_counts
urlpatterns = [
    path('get_batches',get_batches,name='get_batches'),
    path('add_batch',add_batches,name='add_batch'),
    path('get_semesters',get_semesters,name='get_semesters'),
    path('add_semester',add_semester,name='add_semester'),
    path('get_subjects',get_subjects,name='get_subjects'),
    path('add_subjects',add_subjects,name='add_subjects'),
    path('get_teachers',get_teachers,name='get_teachers'),
    path('add_teacher',add_teacher,name='add_teacher'),
    path('add_subjects_to_teacher',add_subjects_to_teacher,name='add_subjects_to_teacher'),
    path('get_object_counts',get_object_counts,name='get_object_counts'),
]
