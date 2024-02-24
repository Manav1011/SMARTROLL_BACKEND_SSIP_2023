from django.urls import path
from .views import create_lecture_session, mark_attendance_for_student,get_session_data_for_export,mark_attendance_for_absent_student
urlpatterns = [     
    path('create_lecture_session/',create_lecture_session,name='create_lecture_session'),
    path('mark_attendance_for_student/',mark_attendance_for_student,name='mark_attendance_for_student'),
    path('mark_attendance_for_absent_student/',mark_attendance_for_absent_student,name='mark_attendance_for_absent_student'),
    path('get_session_data_for_export/<str:session_id>',get_session_data_for_export,name='get_session_data_for_export')
]