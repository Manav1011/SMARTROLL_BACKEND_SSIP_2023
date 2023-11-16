from django.db import models
from Profile.models import Profile
# Create your models here.

class Admin(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.profile.email