from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
import json

# Create your views here.
# postman으로 확인은 안함
def create_matching(request, leader_id, matzip_id):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        
        new_matching = Matching.objects.create(
            leader = get_object_or_404(Profile, pk=leader_id),
            matzip = get_object_or_404(Matzip, pk=matzip_id),
    
            #created_time = models.DateTimeField(auto_now_add=True)
            #is_matched = False,
            #is_closed = False,
            
            bio = body['bio'],
            social_mode = body['social_mode'],
            desired_gender = body['desired_gender'],
            desired_major = body['desired_major'],
            min_people = body['min_people'],
            max_people = body['max_people'],
            date = body['date'],
            start_time =body['start_time'],
            end_time = body['end_time']
        )
        
        new_matzip_json = {
            "leader" : new_matching.leader.nickname,
            "matzip" : new_matching.matzip.name,
            "created_time" : new_matching.created_time,
            "is_matched" : new_matching.is_matching,
            "is_closed" : new_matching.is_closed,
            "bio" : new_matching.bio,
            "social_mode" : new_matching.social.mode,
            "desired_gender" : new_matching.desired_gender,
            "desired_major" : new_matching.desired_major,
            "min_people" : new_matching.min_people,
            "max_people" : new_matching.max_people,
            "date" : new_matching.date,
            "start_time" : new_matching.start_time,
            "end_time" : new_matching.end_time
        }
        return JsonResponse({
            "data" : new_matzip_json
        })

    else:
        return JsonResponse({
            "status" : 405
        })