from django.contrib import admin
from .models import Admin,Teacher,Student,NotificationSubscriptions

# Register your models here.

admin.site.register(Admin)
admin.site.register(Teacher)
admin.site.register(NotificationSubscriptions)

class StudentAdmin(admin.ModelAdmin):
    search_fields = ['enrollment']

admin.site.register(Student,StudentAdmin)