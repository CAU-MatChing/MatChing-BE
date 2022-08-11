from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import *
from matchings.models import *
import json
from datetime import date

# Create your views here.
@require_http_methods(['POST'])  
def create_profile(request):
    if request.method == 'POST':
        #if request.user.is_authenticated:
        body = json.loads(request.body.decode('utf-8'))
            
        new_profile = Profile.objects.create(   
            #account = request.user,
            account = get_object_or_404(Account, pk=body['account_id']),
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
            release_date = date.today()
        )

        new_profile_json = {
            "account" : new_profile.account.email,
            "nickname" : new_profile.nickname,
            "major" : new_profile.major,
            "gender" : new_profile.gender,
            "bio" : new_profile.bio
        }

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "생성 성공",
                "data": new_profile_json
            },
            ensure_ascii=False
        )
                    
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )


    else:
        json_res = json.dumps(
                {
                    "status": 405,
                    "success": False,
                    "message": "method error",
                    "data": None
                },
                ensure_ascii=False
            )
                
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=405
        )

@require_http_methods(['DELETE'])  
def delete_profile(requests, account_id):
    if requests.method =="DELETE":
        delete_profile = get_object_or_404(Profile, pk=id)
        # 특정 profile Delete
        delete_profile.delete()

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "프로필 삭제 성공",
                "data": None
            },
            ensure_ascii=False
            )
                
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )
    else:
        json_res = json.dumps(
                {
                    "status": 405,
                    "success": False,
                    "message": "method error",
                    "data": None
                },
                ensure_ascii=False
            )
                
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=405
        )

@require_http_methods(['GET'])  
def get_my_matchings(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            my_profile = request.user.profile
            matching_json_all=[]
            
            #내가 리더인 경우
            matching_leader_all = Matching.objects.filter(leader = my_profile)    
            for matching in matching_leader_all:
                follower_all = Follower.objects.filter(matching = matching.id)
                
                follower_json_all=[]
                for follower in follower_all:
                    follower_json_all.append(follower.profile.nickname)
                    
                matching_json = {
                    "matching_id" : matching.id,
                    "matzip" : matching.matzip.name,
                    "bio" : matching.bio,
                    "leader" : matching.leader.nickname,
                    "created_time" : matching.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                    #"remain" : matching.max_people-len(follower_json_all),
                    "is_matched" : matching.is_matched,
                    "is_closed" : matching.is_closed,
                    "social_mode" : matching.social_mode,
                    "desired_gender" : matching.desired_gender,
                    "desired_major" : matching.desired_major,
                    "min_people" : matching.min_people,
                    "max_people" : matching.max_people,
                    "start_time" : matching.start_time.strftime("%Y-%m-%d %H:%M"),
                    "end_time" : matching.end_time.strftime("%Y-%m-%d %H:%M"),
                    "duration" : matching.duration,
			        "followers": follower_json_all 
                }
                matching_json_all.append(matching_json)
            
            #내가 팔로워인 경우
            matching_follower_all = Follower.objects.filter(profile = my_profile)
            for matching_follower in matching_follower_all:
                matching = matching_follower.matching
                
                follower_all = Follower.objects.filter(matching = matching.id)
                
                follower_json_all=[]
                for follower in follower_all:
                    follower_json_all.append(follower.profile.nickname)
                    
                matching_json = {
                    "matching_id" : matching.id,
                    "matzip" : matching.matzip.name,
                    "bio" : matching.bio,
                    "leader" : matching.leader.nickname,
                    "created_time" : matching.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                    #"remain" : matching.max_people-len(follower_json_all),
                    "is_matched" : matching.is_matched,
                    "is_closed" : matching.is_closed,
                    "social_mode" : matching.social_mode,
                    "desired_gender" : matching.desired_gender,
                    "desired_major" : matching.desired_major,
                    "min_people" : matching.min_people,
                    "max_people" : matching.max_people,
                    "start_time" : matching.start_time.strftime("%Y-%m-%d %H:%M"),
                    "end_time" : matching.end_time.strftime("%Y-%m-%d %H:%M"),
                    "duration" : matching.duration,
			        "followers": follower_json_all 
                }
                matching_json_all.append(matching_json)

                
            json_res = json.dumps(
                {
                    "status": 200,
                    "success": True,
                    "message": "조회 성공",
                    "data": matching_json_all
                },
                ensure_ascii=False
            )
                
            return HttpResponse(
                json_res,
                content_type=u"application/json; charset=utf-8",
                status=200
            )
                
        
        else:
            json_res = json.dumps(
                    {
                        "status": 401,
                        "success": False,
                        "message": "사용자인증실패",
                        "data": None
                    },
                    ensure_ascii=False
                )
                    
            return HttpResponse(
                json_res,
                content_type=u"application/json; charset=utf-8",
                status=401
            )

    else:
        json_res = json.dumps(
                {
                    "status": 405,
                    "success": False,
                    "message": "method error",
                    "data": None
                },
                ensure_ascii=False
            )
                
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=405
        )
        
@require_http_methods(['GET'])  
def get_nicknames(request):
    if request.method == 'GET':
        #리스트로 닉네임 넣어서 보내기
        profile_all = Profile.objects.all()
        nickname_json_all = []
        
        for profile in profile_all:
            nickname_json_all.append(profile.nickname)
        
        json_res = json.dumps(
                {
                    #"status": 200,
                    "success": True,
                    #"message": "조회 성공",
                    "nickname_list": nickname_json_all
                },
                ensure_ascii=False
            )
                
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )