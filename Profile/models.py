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
    ]
    username = None
    name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(_('email address'),unique=True)
    ph_no = models.CharField(max_length=20)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email