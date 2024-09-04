from django.contrib import admin
from .models import Session,Attendance,Survey,SurveyOption

# Register your models here.

admin.site.register(Session)
admin.site.register(Attendance)
admin.site.register(Survey)
admin.site.register(SurveyOption)