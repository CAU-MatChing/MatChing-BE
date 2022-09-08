from operator import truediv
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import *
from matchings.models import *
import json
from datetime import date,timedelta, datetime

# Create your views here.
@require_http_methods(['POST'])  
def create_profile(request):
    if request.method == 'POST':
        #if request.user.is_authenticated:
        body = json.loads(request.body.decode('utf-8'))
            
        new_profile = Profile.objects.create(   
            #account = request.user,
            account = get_object_or_404(Account, pk=body['accountId']),
            nickname = body['nickname'],
            major = body['major'],
            gender = body['gender'],
                    
            rudeness = 0,
            noshow = 0,
            cancel = 0,
            matching_num = 0,
            matching_people = 0,
            is_disabled = False,
            release_date = date.today()
        )
                    
        return JsonResponse({"success" : True}, status=200)


#민경이 필요없음
@require_http_methods(['DELETE'])  
def delete_profile(requests, account_id):
    if requests.method =="DELETE":
        delete_profile = get_object_or_404(Profile, pk=id)
        # 특정 profile Delete
        delete_profile.delete()

        json_res = json.dumps(
            {
                "success": True
            },
            ensure_ascii=False
            )
                
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )


#매칭 닫혔으나 기간이 지난거를 보여줄지 말지?(성사 안된 매칭)
#닫아준거 보내줄지(어쨌뜬 매칭기간 지난거 보내줄지)
@require_http_methods(['GET'])  
def get_my_matchings(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            my_profile = request.user.profile
            
            # 날짜가 지났으나 마감되지 않은 매칭 닫아주기 - leader
            not_closed_yet_leader = Matching.objects.filter(leader = my_profile, is_closed=False, start_time__range=[datetime.now()-timedelta(days=30),datetime.now()])
            for cur_not_closed_leader in not_closed_yet_leader:
                cur_not_closed_leader.is_closed = True
                cur_not_closed_leader.save()
            
            matching_json_all=[]
            
            #내가 리더인 경우
            matching_leader_all = Matching.objects.filter(leader = my_profile)    
            for matching in matching_leader_all:
                follower_all = Follower.objects.filter(matching = matching.id)
                
                follower_json_all=[]
                for follower in follower_all:
                    follower_json_all.append(follower.profile.nickname)
                    
                matching_json = {
                    "id" : matching.id,
                    "name" : matching.matzip.name,
                    #"bio" : matching.bio,
                    "leader" : matching.leader.nickname,
                    #"created_time" : matching.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                    #"remain" : matching.max_people-len(follower_json_all),
                    #"is_matched" : matching.is_matched,
                    #"is_closed" : matching.is_closed,
                    #"social_mode" : matching.social_mode,
                    #"desired_gender" : matching.desired_gender,
                    #"desired_major" : matching.desired_major,
                    #"min_people" : matching.min_people,
                    #"max_people" : matching.max_people,
                    "date" : matching.start_time.strftime("%Y-%m-%d %H:%M"),
                    #"end_time" : matching.end_time.strftime("%Y-%m-%d %H:%M"),
                    #"duration" : matching.duration,
			        "follower": follower_json_all 
                }
                matching_json_all.append(matching_json)
            
            #내가 팔로워인 경우
            matching_follower_all = Follower.objects.filter(profile = my_profile)
            for matching_follower in matching_follower_all:
                matching = matching_follower.matching
                
                # 날짜가 지났으나 마감되지 않은 매칭 닫아주기 - follower
                if matching.is_closed == False and matching.start_date < datetime.now():
                    matching.is_closed = True
                    matching.save()

                follower_all = Follower.objects.filter(matching = matching.id)
                
                follower_json_all=[]
                for follower in follower_all:
                    follower_json_all.append(follower.profile.nickname)
                
                #보낼때 성사된 매칭만 보내야함? 매칭 진행중인/또는 실패한 매칭도 보내야함?
                matching_json = {
                    "id" : matching.id,
                    "name" : matching.matzip.name,
                    #"bio" : matching.bio,
                    #"created_time" : matching.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                    #"remain" : matching.max_people-len(follower_json_all),
                    #"is_matched" : matching.is_matched,
                    #"is_closed" : matching.is_closed,
                    #"social_mode" : matching.social_mode,
                    #"desired_gender" : matching.desired_gender,
                    #"desired_major" : matching.desired_major,
                    #"min_people" : matching.min_people,
                    #"max_people" : matching.max_people,
                    "date" : matching.start_time.strftime("%Y-%m-%d %H:%M"),
                    #"end_time" : matching.end_time.strftime("%Y-%m-%d %H:%M"),
                    #"duration" : matching.duration,
                    "leader" : matching.leader.nickname,
			        "follower": follower_json_all 
                }
                matching_json_all.append(matching_json)
    
            return HttpResponse(
                json.dumps(
                    {
                        "success" : True,
                        "userMatching" : matching_json_all
                    }, ensure_ascii=False),
                content_type=u"application/json; charset=utf-8",
                status=200
            )
                
        
        else:
            json_res = json.dumps(
                    {
                        "success": False,
                        "errorMessage": "사용자인증실패"
                    },
                    ensure_ascii=False
                )
                    
            return HttpResponse(
                json_res,
                content_type=u"application/json; charset=utf-8",
                status=200
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
                    "success" : True,
                    "nicknameList": nickname_json_all
                },
                ensure_ascii=False
            )
                
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

@require_http_methods(['POST'])
def create_report(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        target = Profile.objects.filter(nickname=body['target'])
        report_type = body["type"]
        matching_id = body["id"]
        reporter = request.user
        duplic = Report.objects.get(id=matching_id, reporter=reporter, target=target)
        
        if duplic != None:
            json_res = json.dumps(
            {
                "success": False,
                "errorMessage" : "중복신고"
            },
            ensure_ascii=False
        )
                    
            return HttpResponse(
                json_res,
                content_type=u"application/json; charset=utf-8",
                status=200
            )
        
        else:
            if report_type == 1: #비매너
                report_type = "rudeness"
                target.rudeness+=1
                # 비매너 횟수 5회 이상이면 일정기간 정지
                if (target.rudeness//5)>=1 and (target.rudeness%3)==0:
                    target.is_disabled = True
                    target.release_date = date.today()+timedelta(weeks=3)
                    target.save()      
            elif report_type == 2: #노쇼
                report_type = "no-show"
                target.noshow+=1
                # 노쇼 횟수 3회 이상이면 일정기간 정지
                if (target.noshow//3)>=1 and (target.noshow%3)==0:
                    target.is_disabled = True
                    target.release_date = date.today()+timedelta(weeks=3)
                    target.save()
                elif (target.noshow//3)>=3 and (target.noshow%3)==0:
                    target.is_disabled = True
                    target.release_date = date.today()+timedelta(weeks=2400)
                    target.save()
            elif report_type == 3: #정보와 다른 사람
                report_type="deception"
                target.is_disabled = True
                target.release_date = date.today()+timedelta(weeks=2400)
                target.save()

            new_report = Report.objects.create(   
                reporter = reporter,
                target = target,
                reason = body['desc'],
                type = report_type,
            )
            json_res = json.dumps(
                {
                    "success": True
                },
                ensure_ascii=False
            )
                        
            return HttpResponse(
                json_res,
                content_type=u"application/json; charset=utf-8",
                status=200
            )