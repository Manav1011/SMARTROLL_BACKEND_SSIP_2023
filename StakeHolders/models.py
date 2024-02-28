from django.db import models
from Profile.models import Profile
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
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Admin, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.profile.email

class Teacher(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)    
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Teacher, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.profile.email if self.profile.email else self.profile.name
    
class Student(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    enrollment  = models.CharField(max_length=12,unique=True)    
    slug = models.SlugField(unique=True, null=True, blank=True)
    sr_no = models.PositiveIntegerField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()                    
        super(Student, self).save(*args, **kwargs)
    
    
    def __str__(self) -> str:
        return self.profile.email if self.profile.email else self.profile.name
