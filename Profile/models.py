from django.db import models
from django.contrib.auth.models import User,AbstractUser
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _



# Create your models here.
# In settings.py AUTH_USER_MODEL = 'yourapp.CustomUserModel'

class Profile(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('technician', 'Technician'),
        ('superadmin', 'Super Admin'),
    ]
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),                
    ]
    username = None
    name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(_('email address'),unique=True,null=True,blank=True)
    ph_no = models.CharField(max_length=20,null=True,blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,null=True,blank=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email if self.email else self.name