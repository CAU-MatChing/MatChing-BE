from django.shortcuts import render
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
            nickname = body['name'],
            major = body['major'],
            gender = body['gender'],
            self_intro = body['self_intro']
        )

        return JsonResponse({
            "status" : 200
        })

    else:
        return JsonResponse({
            "status" : 405
        })