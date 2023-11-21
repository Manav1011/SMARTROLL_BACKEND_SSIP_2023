from django.urls import path
from .views import get_timetable,get_objects_for_lecture,set_lecture_attributes

urlpatterns = [
    path('get_timetable',get_timetable,name='get_timetable'),
    path('get_objects_for_lecture',get_objects_for_lecture,name='get_objects_for_lecture'),
    path('set_lecture_attributes',set_lecture_attributes,name='set_lecture_attributes'),
]
