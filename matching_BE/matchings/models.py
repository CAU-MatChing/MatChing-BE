from django.db import models
from profiles.models import Profile
from matzips.models import Matzip

# Create your models here.
class Matching(models.Model):
    leader = models.ForeignKey(Profile, on_delete=models.CASCADE)
    matzip = models.ForeignKey(Matzip, on_delete=models.CASCADE)
    
    created_time = models.DateTimeField(auto_now_add=True)
    is_matched = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    bio = models.CharField(max_length=60,default='',null=True,blank=True)
    social_mode = models.BooleanField(default=False)
    desired_gender = models.CharField(max_length=1,default='',null=True,blank=True)
    desired_major = models.CharField(max_length=30,default='',null=True,blank=True)
    min_people = models.IntegerField(default=1)
    max_people = models.IntegerField(default=1)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.IntegerField(default=1)


class Follower(models.Model):
    matching = models.ForeignKey(Matching, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)