from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []
    email = None
    name = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    proceed = models.IntegerField(default=0)
