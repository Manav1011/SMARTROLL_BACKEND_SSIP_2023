from django.contrib import admin
from .models import Survey,SurveyOption

# Register your models here.

admin.site.register(Survey)
admin.site.register(SurveyOption)