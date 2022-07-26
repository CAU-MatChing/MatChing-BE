from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
import json

# Create your views here.
def create_profile(request, account_id):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))

        new_profile = Profile.objects.create(   
            account = get_object_or_404(Account,pk=account_id),
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
	        release_date = ''
        )

        new_profile_json = {


        }
        return JsonResponse({
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