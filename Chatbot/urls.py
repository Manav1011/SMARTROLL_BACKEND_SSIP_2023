from django.urls import path
from .views import get_student_attendance_detail_for_subject

urlpatterns = [
    path('get_student_attendance_detail_for_subject/<str:subject_slug>',get_student_attendance_detail_for_subject,name='get_student_attendance_detail_for_subject'),    
    
]