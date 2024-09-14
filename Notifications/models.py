from django.db import models
import uuid,time
from Manage.models import Branch,Subject
from StakeHolders.models import Student

def generate_unique_hash():    
    random_hash = str(uuid.uuid4().int)[:6]    
    timestamp = str(int(time.time()))    
    unique_hash = f"{random_hash}_{timestamp}"
    return unique_hash

# Create your models here.

class Event(models.Model):
    title = models.TextField()
    description = models.TextField()    
    branches = models.ManyToManyField(Branch)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Event, self).save(*args, **kwargs)

class Result(models.Model):
    total_marks = models.PositiveIntegerField()
    gained_marks = models.CharField(max_length=20)
    subject = models.ForeignKey(Subject,on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.student.profile.name} - {self.subject.subject_name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Result, self).save(*args, **kwargs)
