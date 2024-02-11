from django.urls import path
from .views import create_lecture_session, mark_attendance_for_student
urlpatterns = [     
    path('create_lecture_session/',create_lecture_session,name='create_lecture_session'),
    path('mark_attendance_for_student/',mark_attendance_for_student,name='mark_attendance_for_student')
]