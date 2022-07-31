from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
import json

# Create your views here.
def create_profile(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
       
        new_profile = Profile.objects.create(   
            account = request.user,
            nickname = body['nickname'],
            major = body['major'],
            gender = body['gender'],
            bio = body['bio'],
            
            rudeness = 0,
	        noshow = 0,
	        cancel = 0,
	        matching_num = 0,
	        matching_people = 0,
	        is_disabled = False,
	        release_date = '2022-7-28'
        )

        new_profile_json = {
            "account" : new_profile.account.email,
            "nickname" : new_profile.nickname,
            "major" : new_profile.major,
            "gender" : new_profile.gender,
            "bio" : new_profile.bio
        }

        return JsonResponse({
            "status":200,
            "message" : "프로필 생성 성공",
            "data" : new_profile_json
        })

    else:
        return JsonResponse({
            "status" : 405
        })


def delete_profile(requests, account_id):
    if requests.method =="DELETE":
        delete_profile = get_object_or_404(Profile, pk=id)
        # 특정 profile Delete
        delete_profile.delete()

        return JsonResponse({
                'status': 200,
                'success': True,
                'message': 'Delete 성공!',
                'data': None
            })
    else:
        return JsonResponse({
                'status': 405,
                'success': False,
                'message': 'Delete error',
                'data': None
            })