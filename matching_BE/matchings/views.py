from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse,HttpResponse
from .models import Matching, Follower
from profiles.models import Profile
from matzips.models import Matzip
from datetime import datetime, timedelta
import json

def create_matching(request, matzip_id):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        cur_matzip = get_object_or_404(Matzip, pk=matzip_id)
        
        new_matching = Matching.objects.create(
            leader = request.user.profile,
            matzip = cur_matzip,
            bio = body['bio'],
            social_mode = body['social_mode'],
            desired_gender = body['desired_gender'],
            desired_major = body['desired_major'],
            min_people = body['min_people'],
            max_people = body['max_people'],
            start_time = datetime.strptime(body['start_time'], "%Y-%m-%d %H:%M"),
            end_time = datetime.strptime(body['end_time'], "%Y-%m-%d %H:%M")
        )
        
        cur_matzip.waiting+=1
        cur_matzip.save()

        new_matching_json = {
            "leader" : new_matching.leader.nickname,
            "matzip" : new_matching.matzip.name,
            "created_time" : new_matching.created_time.strftime("%Y-%m-%d %H:%M:%S"),
            "is_matched" : new_matching.is_matched,
            "is_closed" : new_matching.is_closed,
            "bio" : new_matching.bio,
            "social_mode" : new_matching.social_mode,
            "desired_gender" : new_matching.desired_gender,
            "desired_major" : new_matching.desired_major,
            "min_people" : new_matching.min_people,
            "max_people" : new_matching.max_people,
            "start_time" : new_matching.start_time.strftime("%Y-%m-%d %H:%M"),
            "end_time" : new_matching.end_time.strftime("%Y-%m-%d %H:%M")
        }

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "생성 성공",
                "data": new_matching_json
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
            "status" : 405
        })
        

@require_http_methods(['GET','PATCH','DELETE'])
def read_update_delete_matching(request, matching_id):
    # 매칭 정보 하나를 불러오는 코드
    if request.method == 'GET':
        get_matching = get_object_or_404(Matching,pk=matching_id)
        follower_json_all = []
        follower_all = Follower.objects.filter(matching = matching_id)

        for follower in follower_all :
            follower_json = {
                "nickname" : follower.profile.nickname,
                "major" : follower.profile.major,
                "gender" : follower.profile.gender
                # 신고 횟수도 반환해야 함
            }
            follower_json_all.append(follower_json)
        
        get_matching_json = {
            "matching_id" : get_matching.id,
            "matzip" : get_matching.matzip.name,
            "bio" : get_matching.bio,
            "leader" : get_matching.leader.nickname,
            "created_time" : get_matching.created_time.strftime("%Y-%m-%d %H:%M:%S"),
            "remain" : get_matching.max_people-len(follower_json_all),
            "is_matched" : get_matching.is_matched,
            "is_closed" : get_matching.is_closed,
            "social_mode" : get_matching.social_mode, # 프론트에서 문자열로 넘겨줄지, 프론트에서 문자열로 바꿀지
            "desired_gender" : get_matching.desired_gender,
            "desired_major" : get_matching.desired_major,
            "min_people" : get_matching.min_people,
            "max_people" : get_matching.max_people,
            "start_time" : get_matching.start_time.strftime("%Y-%m-%d %H:%M"),
            "end_time" : get_matching.end_time.strftime("%Y-%m-%d %H:%M"),
			"followers": follower_json_all 
        }
        
        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "조회 성공",
                "data": get_matching_json
            },
            ensure_ascii=False
        )
            
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

    # 아직 매칭되지 않았을 때 매칭 신청 정보를 수정하는 코드
    elif request.method == "PATCH":
        update_matching = get_object_or_404(Matching, pk=matching_id)
        
        if update_matching.is_matched == False:
            body = json.loads(request.body.decode('utf-8'))
            update_matching.bio = body['bio']
            update_matching.social_mode = body['social_mode']
            update_matching.desired_gender = body['desired_gender']
            update_matching.desired_major = body['desired_major']
            update_matching.min_people = body['min_people']
            update_matching.max_people = body['max_people']
            update_matching.date = body['date']
            update_matching.start_time = body['start_time']
            update_matching.end_time = body['end_time']

            update_matching.save()

            update_matching_json = {
                "matching_id" : update_matching.id,
                "matzip" : update_matching.matzip.name,
                "bio" : update_matching.bio,
                "leader" : update_matching.leader.nickname,
                "social_mode" : update_matching.social_mode, # 프론트에서 문자열로 넘겨줄지, 프론트에서 문자열로 바꿀지
                "desired_gender" : update_matching.desired_gender,
                "desired_major" : update_matching.desired_major,
                "min_people" : update_matching.min_people,
                "max_people" : update_matching.max_people,
                "start_time" : update_matching.start_time.strftime("%Y-%m-%d %H:%M"),
                "end_time" : update_matching.end_time.strftime("%Y-%m-%d %H:%M"),
            }

            json_res = json.dumps(
                {
                    "status": 200,
                    "success": True,
                    "message": "수정 성공",
                    "data": update_matching_json
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
                    "status": 400,
                    "success": False,
                    "message": "매칭 수정 불가",
                    "data": None
                },
                ensure_ascii=False
            )

            return HttpResponse(
                json_res,
                content_type=u"application/json; charset=utf-8",
                status=200
            )


    elif request.method =="DELETE":
        delete_matching = get_object_or_404(Matching, pk=matching_id)
        cur_matzip = get_object_or_404(Matzip, pk=delete_matching.matzip.id)
        delete_matching.delete()
        
        cur_matzip.waiting-=1
        cur_matzip.save()

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "삭제 성공",
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
        return JsonResponse({
                'status': 405,
                'success': False,
                'message': 'Method Error',
                'data': None
            })

@require_http_methods(['POST','DELETE'])
def join_cancel_matching(request, matching_id):
    # 팔로워가 매칭을 신청하는 코드
    if request.method == 'POST':
        # body = json.loads(request.body.decode('utf-8'))
        cur_matching = get_object_or_404(Matching, pk=matching_id)
        
        new_follower = Follower.objects.create(
            matching = cur_matching,
            profile = request.user.profile,
        )

        follower_all = Follower.objects.filter(matching = cur_matching)

        if cur_matching.min_people <= len(follower_all):
            cur_matching.is_matched = True
        else:
            cur_matching.is_matched = False
            
        if cur_matching.max_people <= len(follower_all):
            cur_matching.is_closed = True
        else:
            cur_matching.is_closed = False
        
        cur_matching.save()

        new_follower_json = {
            "matching_id" : matching_id,
            "nickname" : new_follower.profile.nickname,
            "gender" : new_follower.profile.gender,
            "major" : new_follower.profile.major
        }

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "매칭 신청 성공",
                "data": new_follower_json
            },
            ensure_ascii=False
        )
            
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

    
    # 팔로워가 매칭을 취소하는 코드
    elif request.method == 'DELETE':
        cur_matching = get_object_or_404(Matching, pk=matching_id)
        cur_follower = get_object_or_404(Follower, profile=request.user.profile, matching = cur_matching)

        time_now = datetime.now() 
        time_limit = cur_matching.start_time + timedelta(hours=-1)
        

        if time_now < time_limit:
            cur_follower.delete()           
            
            follower_all = Follower.objects.filter(matching = cur_matching)
            if cur_matching.min_people <= len(follower_all):
                cur_matching.is_matched = True
            else:
                cur_matching.is_matched = False
                
            if cur_matching.max_people <= len(follower_all):
                cur_matching.is_closed = True
            else:
                cur_matching.is_closed = False

            cur_matching.save()

            cur_profile = get_object_or_404(Profile, account = request.user)
            cur_profile.cancel+=1
            cur_profile.save()
            
            json_res = json.dumps(
                {
                    "status": 200,
                    "success": True,
                    "message": "삭제 성공",
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
            return JsonResponse({
                'status': 400,
                'success': False,
                'message': '매칭 취소 시간 지남',
                'data': None
            })
