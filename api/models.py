from django.db import models
# Create your models here.

class User(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    value = models.BigIntegerField(default=0)