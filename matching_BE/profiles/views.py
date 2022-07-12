from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
import json

# Create your views here.
def create_profile(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))

        new_profile = Member.objects.create(
            member_id = body['member_id'],
            member_pw = body['member_pw'],
            nickname = body['nickname'],
            major = body['major'],
            gender = body['gender'],
            self_intro = body['self_intro']
        )

        new_profile_json = {
            "member_id" : new_profile.member_id,
            "member_pw" : new_profile.member_pw,
            "nickname" : new_profile.nickname,
            "major" : new_profile.major,
            "gender" : new_profile.gender,
            "self_intro" : new_profile.self_intro
        }
        return JsonResponse({
            "data" : new_profile_json
        })

    else:
        return JsonResponse({
            "status" : 405
        })


def delete_profile(requests, id):
    if requests.method =="DELETE":
        delete_profile = get_object_or_404(Member, pk=id)
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