from django.db import models
import time
import uuid
from datetime import datetime

# Create your models here.

def generate_unique_hash():    
    random_hash = str(uuid.uuid4().int)[:6]    
    timestamp = str(int(time.time()))    
    unique_hash = f"{random_hash}_{timestamp}"
    return unique_hash

class TimeTable(models.Model):
    schedules = models.CharField(max_length=255,default='Not Set Yet')
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            super(TimeTable, self).save(*args, **kwargs)
    

class Subject(models.Model):
    subject_name = models.CharField(max_length=255)
    code = models.IntegerField(unique=True)
    credit = models.IntegerField()
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            super(Subject, self).save(*args, **kwargs)
    

    def __str__(self) -> str:
        return self.subject_name

class Semester(models.Model):
    no = models.IntegerField()
    subjects = models.ManyToManyField(Subject,blank=True)
    status = models.BooleanField(default=True)
    time_table = models.ManyToManyField(TimeTable,blank=True)
    start_date = models.DateField()
    end_date = models.DateField()    
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            super(Semester, self).save(*args, **kwargs)
        today = datetime.today().date()
        if today < self.start_date or today > self.end_date:            
            self.status = False
            super(Semester, self).save(*args, **kwargs)
        else:
            self.status = True
            super(Semester, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Semester - {self.no}"

class Batch(models.Model):
    batch_name = models.CharField(max_length=255)
    semesters = models.ManyToManyField(Semester,blank=True) 
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            super(Batch, self).save(*args, **kwargs)   

    def __str__(self) -> str:
        return self.batch_name

class Branch(models.Model):
    branch_name = models.CharField(max_length=255)
    batches = models.ManyToManyField(Batch,blank=True)
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            super(Branch, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.branch_name

class College(models.Model):
    college_name = models.CharField(max_length=255)
    branches = models.ManyToManyField(Branch,blank=True)
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            super(College, self).save(*args, **kwargs)
    

    def __str__(self) -> str:
        return self.college_name
