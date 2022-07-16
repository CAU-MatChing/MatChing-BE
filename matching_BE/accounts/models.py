from django.db import models

# Create your models here.
class Account(models.Model):
    email = models.CharField(max_length=50,unique=True,null=False,blank=False)
    password = models.CharField(max_length=20,null=False,blank=False)
    is_approved = models.BooleanField(default=False)