from django.db import models
from StakeHolders.models import Student
import uuid,time

def generate_unique_hash():    
    random_hash = str(uuid.uuid4().int)[:6]    
    timestamp = str(int(time.time()))    
    unique_hash = f"{random_hash}_{timestamp}"
    return unique_hash

# Create your models here.

SURVEY_TYPES = [
    ('mcq','Multiple Choices'),
    ('desc','Descriptive')
]

SURVEY_CHOICES = [
    ('single','Single Choice'),
    ('multiple','Multiple Choice')
]


class SurveyOption(models.Model):
    option = models.TextField()
    student = models.ManyToManyField(Student,blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(SurveyOption, self).save(*args, **kwargs)


class Survey(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=4, choices=SURVEY_TYPES,default='mcq')
    allowd_choices = models.CharField(max_length=8,choices=SURVEY_CHOICES,default='single')
    lecture = models.ForeignKey(Lecture,on_delete=models.CASCADE,null=True,blank=True)
    options = models.ManyToManyField(SurveyOption,blank=True)
    allowed_students = models.ManyToManyField(Student,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.type}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Survey, self).save(*args, **kwargs)
