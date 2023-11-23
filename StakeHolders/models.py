from django.db import models
from Profile.models import Profile
from Manage.models import Subject,Branch,Semester
import uuid
import time

def generate_unique_hash():    
    random_hash = str(uuid.uuid4().int)[:6]    
    timestamp = str(int(time.time()))    
    unique_hash = f"{random_hash}_{timestamp}"
    return unique_hash
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
    
class Student(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    enrollment  = models.CharField(max_length=12,unique=True)
    signature_link = models.TextField(null=True,blank=True)
    subjects = models.ManyToManyField(Subject,blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.DO_NOTHING,null=True,blank=True)
    semester = models.ForeignKey(Semester,on_delete=models.DO_NOTHING,null=True,blank=True)
    thank_you_response = models.TextField(null=True,blank=True)
    steps = models.IntegerField(null=True,blank=True,default=1)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            super(Student, self).save(*args, **kwargs)
        else:
            super(Student, self).save(*args, **kwargs)
    
    
    def __str__(self) -> str:
        return self.profile.email
