from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
# cy : change email, password null=True

# 수정해야댐
class Account(AbstractBaseUser):
    email = models.CharField(max_length=50,unique=True,null=True)
    #password = models.CharField(max_length=20,null=True)
    is_active = models.BooleanField(default=False)