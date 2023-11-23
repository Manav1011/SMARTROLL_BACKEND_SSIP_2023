from django.urls import path
from .views import get_todays_timetable_for_student,get_todays_timetable_for_teacher

urlpatterns = [
    path('get_todays_timetable_for_student',get_todays_timetable_for_student),
    path('get_todays_timetable_for_teacher',get_todays_timetable_for_teacher)
]
