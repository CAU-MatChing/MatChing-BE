from django.db import models
from accounts.models import Account

# Create your models here.
class Profile(models.Model):
	account = models.ForeignKey(Account, on_delete=models.CASCADE)
	nickname = models.CharField(max_length=18, unique=True)
	major = models.CharField(max_length=30)
	gender = models.CharField(max_length=1)
	bio = models.CharField(max_length=60, null=True, blank=True)
 
	rudeness = models.IntegerField(default=0)
	noshow = models.IntegerField(default=0)
	cancel = models.IntegerField(default=0)
	matching_num = models.IntegerField(default=0)
	matching_people = models.IntegerField(default=0)
	is_disabled = models.BooleanField(default=False)
	release_date = models.CharField(max_length=10, default='', blank=True, null=True)
 
 
	
		
		