from django.db import models
import time
import uuid
from datetime import datetime
from TimeTable.models import Timetable

# Create your models here.

def generate_unique_hash():    
    random_hash = str(uuid.uuid4().int)[:6]    
    timestamp = str(int(time.time()))    
    unique_hash = f"{random_hash}_{timestamp}"
    return unique_hash

    
class Subject(models.Model):
    subject_name = models.CharField(max_length=255)
    code = models.IntegerField(unique=True)
    credit = models.IntegerField()
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            super(Subject, self).save(*args, **kwargs)
        else:
            self.status = True
            super(Subject, self).save(*args, **kwargs)
    

    def __str__(self) -> str:
        return self.subject_name

class Semester(models.Model):
    no = models.IntegerField()
    subjects = models.ManyToManyField(Subject,blank=True)
    status = models.BooleanField(default=True)
    time_table = models.ManyToManyField(Timetable,blank=True)
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
    start_year = models.CharField(max_length=4,blank=True,null=True)
    end_year = models.CharField(max_length=4,blank=True,null=True)
    semesters = models.ManyToManyField(Semester,blank=True) 
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            start_year = datetime.strptime(self.start_year, '%Y').year            
            end_year = datetime.strptime(self.end_year, '%Y').year
            current_year = datetime.now().year
            if current_year != start_year and end_year != current_year + 1:                
                self.active = False                
            else:
                self.active == True                
            super(Batch, self).save(*args, **kwargs) 
        else:
            super(Batch, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.batch_name

class Branch(models.Model):
    branch_name = models.CharField(max_length=255)
    batches = models.ManyToManyField(Batch,blank=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    branch_code = models.IntegerField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            super(Branch, self).save(*args, **kwargs)
        else:
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
        else:
            super(College, self).save(*args, **kwargs)
            
    

    def __str__(self) -> str:
        return self.college_name
