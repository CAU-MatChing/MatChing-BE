from re import X
from django.db import models
from accounts.models import Account

class Profile(models.Model):
	account = models.OneToOneField(Account, on_delete=models.CASCADE)
	nickname = models.CharField(max_length=18, unique=True)
	major = models.CharField(max_length=30)
	gender = models.CharField(max_length=1)
 
	rudeness = models.IntegerField(default=0)
	noshow = models.IntegerField(default=0)
	cancel = models.IntegerField(default=0)
	matching_num = models.IntegerField(default=0)
	matching_people = models.IntegerField(default=0)
	is_disabled = models.BooleanField(default=False)
	release_date = models.DateField()
	
	def __str__(self):
		return self.nickname

class Report(models.Model):
	TYPE_CHOICES = (
		('no-show','노쇼'),
		('rudeness','비매너'),
		('deception','정보와 다른 사람'),
	)
	type = models.CharField(max_length=31,default='',choices=TYPE_CHOICES)
	reporter = models.ForeignKey(Profile,related_name="reporter", on_delete=models.PROTECT)
	target = models.ForeignKey(Profile, related_name="target",on_delete=models.PROTECT)
	reason = models.TextField()

		