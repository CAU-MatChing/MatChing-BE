from django.db import models

# Create your models here.
# cy : change email, password null=True
class Account(models.Model):
    email = models.CharField(max_length=50,unique=True,null=True)
    password = models.CharField(max_length=20,null=True)
    is_active = models.BooleanField(default=False)