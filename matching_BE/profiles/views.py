from operator import truediv
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import *
from matchings.models import *
import json
from datetime import date,timedelta, datetime
from django.db.models import Q

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
            matching_leader_all = Matching.objects.filter(Q(leader = my_profile) & ~Q(is_matched=False, is_closed=True))
             
            for matching in matching_leader_all:
                follower_all = Follower.objects.filter(matching = matching.id)
                
                member_json_all=[]
                for follower in follower_all:
                    member_json_all.append(follower.profile.nickname)
                
                
                matching_json = {
                    "id" : matching.id,
                    "name" : matching.matzip.name,
                    #"bio" : matching.bio,
                    #"created_time" : matching.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                    #"remain" : matching.max_people-len(follower_json_all),
                    "is_matched" : matching.is_matched,
                    "is_closed" : matching.is_closed,
                    #"social_mode" : matching.social_mode,
                    #"desired_gender" : matching.desired_gender,
                    #"desired_major" : matching.desired_major,
                    #"min_people" : matching.min_people,
                    #"max_people" : matching.max_people,
                    "date" : matching.start_time.strftime("%Y-%m-%d %H:%M"),
                    #"end_time" : matching.end_time.strftime("%Y-%m-%d %H:%M"),
                    #"duration" : matching.duration,
                    #"leader" : matching.leader.nickname,
			        #"follower": follower_json_all,
                    "member" : member_json_all
                }
                matching_json_all.append(matching_json)
            
            #내가 팔로워인 경우
            matching_follower_all = Follower.objects.filter(profile = my_profile)
            for matching_follower in matching_follower_all:
                matching = matching_follower.matching
                
                # 날짜가 지났으나 마감되지 않은 매칭 닫아주기 - follower
                if matching.is_closed == False and matching.start_time < datetime.now():
                    matching.is_closed = True
                    matching.save()

                #is_closed=true, is_matched=false 걸러줘야 한다.
                if(matching.is_matched == False and matching.is_closed == True):
                    pass
                else:
                    follower_all = Follower.objects.filter(matching = matching.id)
                    
                    member_json_all=[]
                    member_json_all.append(matching.leader.nickname)
                    #follower_json_all=[]
                    for follower in follower_all:
                        if follower.profile.nickname != my_profile.nickname:
                            member_json_all.append(follower.profile.nickname)
                    
                   
                    matching_json = {
                        "id" : matching.id,
                        "name" : matching.matzip.name,
                        #"bio" : matching.bio,
                        "is_matched" : matching.is_matched,
                        "is_closed" : matching.is_closed,
                        #"social_mode" : matching.social_mode,
                        #"desired_gender" : matching.desired_gender,
                        #"desired_major" : matching.desired_major,
                        #"min_people" : matching.min_people,
                        #"max_people" : matching.max_people,
                        "date" : matching.start_time.strftime("%Y-%m-%d %H:%M"),
                        #"end_time" : matching.end_time.strftime("%Y-%m-%d %H:%M"),
                        #"duration" : matching.duration,
                        #"leader" : matching.leader.nickname,
                        #"follower": follower_json_all,
                        "member" : member_json_all 
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
        target_profile = Profile.objects.get(nickname=body['target'])
        report_type = body["type"]
        matching_id = body["id"]
        reporter_profile = request.user.profile
        #duplic = Report.objects.get(id=matching_id, reporter=reporter, target=target)
        try:
            duplic = Report.objects.get(id=matching_id, reporter=reporter_profile, target=target_profile)
        except Report.DoesNotExist:
            duplic = None
        
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
                target_profile.rudeness+=1
                # 비매너 횟수 5회 이상이면 일정기간 정지
                if (target_profile.rudeness//5)>=1 and (target_profile.rudeness%3)==0:
                    target_profile.is_disabled = True
                    target_profile.release_date = date.today()+timedelta(weeks=3)
                    target_profile.save()      
            elif report_type == 2: #노쇼
                report_type = "no-show"
                target_profile.noshow+=1
                # 노쇼 횟수 3회 이상이면 일정기간 정지
                if (target_profile.noshow//3)>=1 and (target_profile.noshow%3)==0:
                    target_profile.is_disabled = True
                    target_profile.release_date = date.today()+timedelta(weeks=3)
                    target_profile.save()
                elif (target_profile.noshow//3)>=3 and (target_profile.noshow%3)==0:
                    target_profile.is_disabled = True
                    target_profile.release_date = date.today()+timedelta(weeks=2400)
                    target_profile.save()
            elif report_type == 3: #정보와 다른 사람
                report_type="deception"
                target_profile.is_disabled = True
                target_profile.release_date = date.today()+timedelta(weeks=2400)
                target_profile.save()

            new_report = Report.objects.create(   
                reporter = reporter_profile,
                target = target_profile,
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