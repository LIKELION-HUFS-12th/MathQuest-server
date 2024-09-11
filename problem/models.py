from django.db import models

# Create your models here.
class Problem(models.Model):
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=2)
    solution = models.CharField(max_length=400)
    choice1 = models.CharField(max_length=50)
    choice2 = models.CharField(max_length=50)
    choice3 = models.CharField(max_length=50)
    choice4 = models.CharField(max_length=51)
    difficulty = models.CharField(max_length=100)
    level = models.CharField(max_length=20)
    chapter = models.CharField(max_length=20)
    point = models.IntegerField()