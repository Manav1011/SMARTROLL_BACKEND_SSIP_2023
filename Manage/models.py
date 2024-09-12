from django.db import models
import time
import uuid
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from StakeHolders.models import Teacher,Student,Admin

# Create your models here.

def generate_unique_hash():    
    random_hash = str(uuid.uuid4().int)[:6]    
    timestamp = str(int(time.time()))    
    unique_hash = f"{random_hash}_{timestamp}"
    return unique_hash


class College(models.Model):
    college_name = models.CharField(max_length=255)    
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(College, self).save(*args, **kwargs)                    
            
    

    def __str__(self) -> str:
        return self.college_name
    
class Branch(models.Model):
    branch_name = models.CharField(max_length=255)    
    branch_code = models.CharField(unique=True,null=True,blank=True,max_length=3)
    slug = models.SlugField(unique=True,null=True,blank=True)
    college = models.ForeignKey(College,on_delete=models.CASCADE)
    admins = models.ManyToManyField(Admin,blank=True)
    teachers = models.ManyToManyField(Teacher,blank=True)
    students = models.ManyToManyField(Student,blank=True)    


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Branch, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.branch_name

TERM_TYPE = [
    ('even','Even'),
    ('odd','Odd'),    
]


class Term(models.Model):
    start_year = models.PositiveIntegerField(validators = [MinValueValidator(1900),MaxValueValidator(2100)],null=True,blank=True)
    end_year = models.PositiveIntegerField(validators = [MinValueValidator(1900),MaxValueValidator(2100)],null=True,blank=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    type = models.CharField(max_length=4,choices = TERM_TYPE,null=True,blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,blank=True,null=True)
    status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Term, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Term - {self.start_year} | {self.end_year}"

class Semester(models.Model):
    no = models.IntegerField()    
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    term = models.ForeignKey(Term,on_delete=models.CASCADE,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Semester, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Semester - {self.no}"
    
class Division(models.Model):
    division_name = models.CharField(max_length=2)
    slug = models.SlugField(unique=True,null=True,blank=True)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Division, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Division - {self.division_name}"
    

class Batch(models.Model):
    batch_name = models.CharField(max_length=10)
    slug = models.SlugField(unique=True,null=True,blank=True)
    division = models.ForeignKey(Division,on_delete=models.CASCADE)
    students = models.ManyToManyField(Student,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Batch, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Division - {self.division.division_name} | {self.batch_name}"
    
class Subject(models.Model):
    subject_name = models.CharField(max_length=255)
    code = models.CharField(unique=True,max_length=20,null=True,blank=True)
    credit = models.IntegerField()
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE,blank=True,null=True)    
    included_batches = models.ManyToManyField(Batch,blank=True)
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()                                
        super(Subject, self).save(*args, **kwargs)
    

    def __str__(self) -> str:
        return self.subject_name
    
class TimeTable(models.Model):
    division = models.ForeignKey(Division,on_delete=models.CASCADE)
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(TimeTable, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Division - {self.slug}"
    
class GPSCoordinates(models.Model):
    title = models.CharField(max_length=255,null=True,blank=True)
    long = models.CharField(max_length=255,null=True,blank=True)
    latt = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self) -> str:
        return self.title if self.title else 'None'



class Classroom(models.Model):
    class_name = models.CharField(max_length = 20)    
    slug = models.SlugField(unique=True,null=True,blank=True)
    branch = models.ForeignKey(Branch,null=True,blank=True,on_delete=models.CASCADE)
    gps_coordinates = models.ForeignKey(GPSCoordinates,blank=True,null=True,on_delete=models.DO_NOTHING)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Classroom, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.class_name


LECTURE_TYPE = [
        ('lab', 'Lab'),
        ('theory', 'Theory'),
]

class Schedule(models.Model):
    day = models.CharField(max_length=10,null=True,blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    timetable = models.ForeignKey(TimeTable,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Schedule, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.day

class Lecture(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    type = models.CharField(max_length=6,choices=LECTURE_TYPE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE, null=True,blank=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE, null=True,blank=True)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE, null=True,blank=True)
    batches = models.ManyToManyField(Batch, blank=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.DO_NOTHING, null=True,blank=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    is_proxy = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Lecture, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.type} - {self.subject.subject_name}"
    
class Link(models.Model):
    from_lecture = models.ForeignKey(Lecture, null=True, blank=True, on_delete=models.CASCADE, related_name='from_links')
    to_lecture = models.ForeignKey(Lecture, null=True, blank=True, on_delete=models.CASCADE, related_name='to_links')
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Link, self).save(*args, **kwargs)