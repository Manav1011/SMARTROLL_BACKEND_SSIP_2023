from django.db import models
import hashlib
import secrets
from Manage.models import Lecture
from StakeHolders.models import Student



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
    marking_ip = models.GenericIPAddressField(null=True,blank=True)
    # physically_present = models.BooleanField(default=False)


class Session(models.Model):
    session_id = models.TextField(unique=True)
    lecture = models.OneToOneField(Lecture,on_delete=models.CASCADE,null=True,blank=True,unique=True)    
    attendances = models.ManyToManyField(Attendance,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.session_id:
            self.session_id = generate_random_unique_hash()
        super(Session, self).save(*args, **kwargs)


