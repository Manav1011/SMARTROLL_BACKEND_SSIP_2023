from django.contrib import admin
from .models import Survey,SurveyOption,StudyMaterial,StudyMaterial_Link

# Register your models here.

admin.site.register(Survey)
admin.site.register(SurveyOption)
admin.site.register(StudyMaterial)
admin.site.register(StudyMaterial_Link)