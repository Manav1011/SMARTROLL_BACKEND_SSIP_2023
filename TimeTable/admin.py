from django.contrib import admin
from .models import Timetable,Schedule,Lecture,Classroom,Router

# Register your models here.

admin.site.register(Timetable)
admin.site.register(Schedule)
admin.site.register(Lecture)
admin.site.register(Classroom)
admin.site.register(Router)