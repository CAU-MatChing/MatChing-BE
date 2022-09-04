from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse,HttpResponse
from datetime import datetime, timedelta
from .models import *
from matchings.models import *
import json

@require_http_methods(['POST'])
def create_matzip(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            body = json.loads(request.body.decode('utf-8'))
            
            if Matzip.objects.filter(name = body['name']).exists():
                json_res = json.dumps(
                        {
                            "success": False,
                            "errorMessage": "식당 이름 중복"
                        },
                        ensure_ascii=False
                    )

                return HttpResponse(
                    json_res,
                    content_type=u"application/json; charset=utf-8",
                    status=400
                )

            new_matzip = Matzip.objects.create(
                name = body['name'],
                waiting = 0
            )

            return HttpResponse(
                json.dumps({"success" : True}, ensure_ascii=False),
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
                status=401
            )


#민경이가 안쓸듯
@require_http_methods(['DELETE','GET'])  
def get_delete_matzip(request, id):
    if request.method == "GET":
        get_matzip = get_object_or_404(Matzip, pk=id)
        
        get_matzip_json = {
            "name" : get_matzip.name,
            "waiting" : get_matzip.waiting
        }
            
        return HttpResponse(
            json.dumps(get_matzip_json,ensure_ascii=False),
            content_type=u"application/json; charset=utf-8",
            status=200
        )

    elif request.method =="DELETE":
        delete_matzip = get_object_or_404(Matzip, pk=id)
        delete_matzip.delete()

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

# 현재 맛집 및 매칭 정보 응답
@require_http_methods(['GET'])  
def getall_now_matzip(request):
    if request.method == "GET":
        not_closed_yet = Matching.objects.filter(is_closed=False, start_time__range=[datetime.now()-timedelta(days=30),datetime.now()])
        
        # 날짜가 지났으나 마감되지 않은 매칭 닫아주기
        for cur_not_closed in not_closed_yet:
            cur_not_closed.is_closed = True
            cur_not_closed.save()

        now_matzip_all = Matzip.objects.all()

        now_matzip_json_all = []
        for now_matzip in now_matzip_all:
            now_matching_all = Matching.objects.filter(matzip = now_matzip.id, is_closed = False,start_time__range=[datetime.now()+timedelta(seconds=1),datetime.now()+timedelta(days=30)])
            
            # 맛집 대기팀 수(waiting) 갱신
            now_matzip.waiting = now_matching_all.count()
            now_matzip.save()

            now_matching_json_all=[]
            for now_matching in now_matching_all:
                now_follower_all = Follower.objects.filter(matching = now_matching.id)
                
                now_follower_json_all=[]
                for now_follower in now_follower_all:
                    now_follower_json_all.append(now_follower.profile.nickname)
                
                #gender, mode는 우리쪽에서 한글로 바꿔서 보낼수도 있음
                tag = [now_matching.desired_gender,now_matching.desired_major,now_matching.social_mode]
                now_matching_json = {
                    "tags" : tag,
                    "startTime" : now_matching.start_time.strftime("%Y-%m-%d %H:%M"),
                    "endTime" : now_matching.end_time.strftime("%Y-%m-%d %H:%M"),
                    "duration" : now_matching.duration,
                    "max" : now_matching.max_people,
                    "min" : now_matching.min_people, #민경이쪽 빠진거
                    "id" : now_matching.id,
                    "description" : now_matching.bio,
                    "leader" : now_matching.leader.nickname, #민경이쪽 빠진거
                    "created_time" : now_matching.created_time.strftime("%Y-%m-%d %H:%M:%S"), #민경이쪽 빠진거
                    # "remain" : now_matching.max_people-len(now_follower_json_all),
                    "is_matched" : now_matching.is_matched, #민경이쪽 빠진거
                    "is_closed" : now_matching.is_closed, #민경이쪽 빠진거
			        "follower": now_follower_json_all #리더랑 합쳐서 보낼지 합의/따로보낼지
                }
                now_matching_json_all.append(now_matching_json)
                
            now_matzip_json = {
                "name" : now_matzip.name,
                "waiting" : now_matzip.waiting,
                "matchings" : now_matching_json_all
            }
            now_matzip_json_all.append(now_matzip_json)

        json_res = json.dumps(
            {
                "success" : True,
                "matchingList" : now_matzip_json_all
            },
            ensure_ascii=False
        )  

        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )