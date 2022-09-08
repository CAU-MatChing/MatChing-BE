from django.db import models

# Create your models here.
class Matzip(models.Model):
    name = models.CharField(max_length=60,null=True,default='', unique=True)
    waiting = models.IntegerField(default=0)
    matched = models.IntegerField(default=0)