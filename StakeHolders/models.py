from django.db import models
from Profile.models import Profile
from Manage.models import Subject,Branch
# Create your models here.

class Admin(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self) -> str:
        return self.profile.email

class Teacher(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject,blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self) -> str:
        return self.profile.email