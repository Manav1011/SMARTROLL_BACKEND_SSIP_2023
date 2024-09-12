from django.db import models
from StakeHolders.models import Student,Teacher
from Manage.models import Subject
import uuid,time
from django.db.models.signals import pre_delete
from django.dispatch import receiver

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
    options = models.ManyToManyField(SurveyOption,blank=True)
    allowed_students = models.ManyToManyField(Student,blank=True)
    owner = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.type}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Survey, self).save(*args, **kwargs)

@receiver(pre_delete, sender=Survey)
def pre_delete_session(sender, instance, **kwargs):    
    instance.options.all().delete()


class StudyMaterial(models.Model):
    title = models.TextField()
    link = models.URLField()
    subject = models.ForeignKey(Subject,on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(StudyMaterial, self).save(*args, **kwargs)
