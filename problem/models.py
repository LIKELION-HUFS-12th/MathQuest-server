from django.db import models
from users.models import CustomUser
# Create your models here.
class Problem(models.Model):
    STATUS_CHOICES = [
        ('RIGHT', '맞은 문제'),
        ('WRONG', '틀린 문제'),
        ('YET', '아직 안 푼 문제'),
    ]
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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='YET') 

    # problem/models.py
class UserProblem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Problem.STATUS_CHOICES)
