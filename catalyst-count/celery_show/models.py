from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    existingPath = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=150)
    eof = models.BooleanField()
    file = models.FileField(upload_to='uploads/')


class UploadedFile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    year_founded = models.IntegerField()
    industry = models.CharField(max_length=255)
    size_range = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    linkedin_url = models.URLField()
    current_employee_estimate = models.IntegerField()
    total_employee_estimate = models.IntegerField()

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='Active')

    def __str__(self):
        return self.user.username    
 