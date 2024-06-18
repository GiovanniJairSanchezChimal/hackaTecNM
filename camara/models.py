
from django.db import models
from django.contrib.auth.models import User

class Questionnaire(models.Model):
    question1 = models.TextField(max_length=100)
    question2 = models.TextField(max_length=100)
    question3 = models.TextField(max_length=100)
    question4 = models.TextField(max_length=100)
    question5 = models.TextField(max_length=100)

