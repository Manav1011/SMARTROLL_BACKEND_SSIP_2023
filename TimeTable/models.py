from django.db import models
import uuid
import time
from Session.models import Session

def generate_unique_hash():    
    random_hash = str(uuid.uuid4().int)[:6]    
    timestamp = str(int(time.time()))    
    unique_hash = f"{random_hash}_{timestamp}"
    return unique_hash

class Router(models.Model):
    default_gateway_address = models.GenericIPAddressField()
    mac_add = models.CharField(max_length=17)
    capacity = models.IntegerField()
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            super(Router, self).save(*args, **kwargs)
        else:
            super(Router, self).save(*args, **kwargs)
    def __str__(self) -> str:
        return self.mac_add

class Classroom(models.Model):
    branch = models.ForeignKey('Manage.Branch', on_delete=models.DO_NOTHING)
    class_name = models.CharField(max_length=255, unique=True)
    routers = models.ManyToManyField(Router,blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            super(Classroom, self).save(*args, **kwargs)
        else:
            super(Classroom, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.class_name

class Lecture(models.Model):
    subject = models.ForeignKey('Manage.Subject', on_delete=models.DO_NOTHING,blank=True,null=True)
    teacher = models.ForeignKey('StakeHolders.Teacher',on_delete=models.DO_NOTHING,blank=True,null=True)
    teacher_proxy = models.ForeignKey('StakeHolders.Teacher',on_delete=models.DO_NOTHING,blank=True,null=True,related_name='proxy')
    classroom = models.ForeignKey(Classroom, on_delete=models.DO_NOTHING,blank=True,null=True)
    start_time = models.TimeField(blank=True,null=True)
    end_time = models.TimeField(blank=True,null=True)
    session = models.ForeignKey(Session,on_delete=models.SET_NULL,null=True,blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            super(Lecture, self).save(*args, **kwargs)
        else:
            super(Lecture, self).save(*args, **kwargs)
    def __str__(self) -> str:
        return f"{self.start_time} {self.end_time}"

class Schedule(models.Model):
    day = models.CharField(max_length=10,null=True,blank=True)
    lectures = models.ManyToManyField(Lecture, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            super(Schedule, self).save(*args, **kwargs)
        else:
            super(Schedule, self).save(*args, **kwargs)
    def __str__(self) -> str:
        return self.day

    
class Timetable(models.Model):
    schedules = models.ManyToManyField(Schedule, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            super(Timetable, self).save(*args, **kwargs)
        else:
            super(Timetable, self).save(*args, **kwargs)
    
    def __str__(self) -> str:        
        return self.slug