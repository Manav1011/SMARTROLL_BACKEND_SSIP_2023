from django.db import models

# Create your models here.

class TimeTable(models.Model):
    schedules = models.CharField(max_length=255,default='Not Set Yet')

class Subject(models.Model):
    subject_name = models.CharField(max_length=255)
    code = models.IntegerField()
    credit = models.IntegerField()

    def __str__(self) -> str:
        return self.subject_name

class Semester(models.Model):
    no = models.IntegerField()
    subjects = models.ManyToManyField(Subject,blank=True)
    status = models.BooleanField(default=True)
    time_table = models.ManyToManyField(TimeTable,blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str:
        return f"Semester - {self.no}"

class Batch(models.Model):
    batch_name = models.CharField(max_length=255)
    semesters = models.ManyToManyField(Semester,blank=True)

    def __str__(self) -> str:
        return self.batch_name

class Branch(models.Model):
    branch_name = models.CharField(max_length=255)
    batches = models.ManyToManyField(Batch,blank=True)

    def __str__(self) -> str:
        return self.branch_name

class College(models.Model):
    college_name = models.CharField(max_length=255)
    branches = models.ManyToManyField(Branch,blank=True)

    def __str__(self) -> str:
        return self.college_name
