from django.contrib import admin
from .models import College,Branch,Batch,Semester,Subject

# Register your models here.

admin.site.register(College)
admin.site.register(Branch)
admin.site.register(Batch)
admin.site.register(Semester)
admin.site.register(Subject)