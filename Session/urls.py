from django.urls import path
from .views import create_lecture_session
urlpatterns = [     
    path('create_lecture_session/',create_lecture_session,name='create_lecture_session')
]