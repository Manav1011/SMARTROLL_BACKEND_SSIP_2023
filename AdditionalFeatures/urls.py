from django.urls import path
from .views import generate_survey_for_a_lecture,get_surveys_of_the_teacher,get_surveys_of_the_student,upload_study_material,get_study_material_for_students
urlpatterns = [     
    path('generate_survey_for_a_lecture/',generate_survey_for_a_lecture,name='generate_survey_for_a_lecture'),    
    path('get_surveys_of_the_teacher',get_surveys_of_the_teacher,name='get_surveys_of_the_teacher'),
    path('get_surveys_of_the_student',get_surveys_of_the_student,name='get_surveys_of_the_student'),
    path('upload_study_material/',upload_study_material,name='upload_study_material'),
    path('get_study_material_for_students',get_study_material_for_students,name='get_study_material_for_students'),
]