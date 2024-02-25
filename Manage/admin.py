from django.contrib import admin
from .models import Subject,College,Branch,Semester,Division,Batch,TimeTable,Schedule,Classroom,Lecture,Term,Link,GPSCoordinates

# Register your models here.

admin.site.register(Subject)
admin.site.register(College)
admin.site.register(Branch)
admin.site.register(Semester)
admin.site.register(Division)
admin.site.register(Batch)
admin.site.register(TimeTable)
admin.site.register(Schedule)
admin.site.register(Classroom)
admin.site.register(Lecture)
admin.site.register(Term)
admin.site.register(Link)
admin.site.register(GPSCoordinates)