from django.db import models
import hashlib
import secrets
from Manage.models import Lecture,GPSCoordinates
from StakeHolders.models import Student
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import uuid,time

def generate_unique_hash():    
    random_hash = str(uuid.uuid4().int)[:6]    
    timestamp = str(int(time.time()))    
    unique_hash = f"{random_hash}_{timestamp}"
    return unique_hash

# Create your models here.
def generate_random_unique_hash():
    # Generate a random string using secrets module
    random_string = secrets.token_hex(16)  # You can adjust the length as needed

    # Create a new SHA-256 hash object
    sha256 = hashlib.sha256()

    # Update the hash object with the bytes-like object of the random string
    sha256.update(random_string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hash_result = sha256.hexdigest()

    return hash_result

class Attendance(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)
    marking_time = models.DateTimeField(null=True,blank=True)    
    manual = models.BooleanField(default=False)
    coordinates = models.ForeignKey(GPSCoordinates,on_delete = models.DO_NOTHING,null=True,blank=True)
    on_premises = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Attendance, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.student.profile.name if self.student.profile.name else self.id

SESSION_STATUS = [
    ('pre','Pre'),
    ('ongoing','Ongoing'),
    ('post','Post')
]


class Session(models.Model):
    day = models.DateField(null=True,blank=True)
    session_id = models.TextField(unique=True)
    lecture = models.ForeignKey(Lecture,on_delete=models.CASCADE,null=True,blank=True)
    attendances = models.ManyToManyField(Attendance,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.CharField(max_length=7,choices = SESSION_STATUS,null=True,blank=True)    


    def save(self, *args, **kwargs):
        if not self.session_id:
            self.session_id = generate_random_unique_hash()
        super(Session, self).save(*args, **kwargs)    

@receiver(pre_delete, sender=Session)
def pre_delete_session(sender, instance, **kwargs):    
    instance.attendances.all().delete()

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
