from django.urls import path
from .views import get_student_attendance_detail_for_subject,get_result_of_student_by_subject

urlpatterns = [
    path('get_student_attendance_detail_for_subject/<str:subject_slug>',get_student_attendance_detail_for_subject,name='get_student_attendance_detail_for_subject'),    
    path('get_result_of_student_by_subject/<str:subject_slug>',get_result_of_student_by_subject,name='get_result_of_student_by_subject'),    
    
]