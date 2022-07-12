from django.db import models

# Create your models here.
class Member(models.Model):
		member_id = models.CharField(max_length=20,unique=True)
		member_pw = models.CharField(max_length=20)
		nickname = models.CharField(max_length=18, unique=True)
		major = models.CharField(max_length=30)
		gender = models.CharField(max_length=1)
		self_intro = models.CharField(max_length=60, null=True, blank=True)
		
		