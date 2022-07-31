from django.db import models

# Create your models here.
class Matzip(models.Model):
    name = models.CharField(max_length=60,null=True,default='', unique=True)
    location = models.TextField(blank=True,default='')
    waiting = models.IntegerField(default=0)