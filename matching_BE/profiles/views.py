from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import *
from matchings.models import *
import json

# Create your views here.
def create_profile(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
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
            'status' : 401,
            'success': False,
            'message': '사용자인증실패',
            'data': None
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
            return JsonResponse({
                'status' : 401,
                'success': False,
                'message': '사용자인증실패',
                'data': None
            })

    else:
        return JsonResponse({
            "status" : 405
        })