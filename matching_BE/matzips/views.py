from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse,HttpResponse
from datetime import datetime, timedelta
from .models import *
from matchings.models import *
import json

@require_http_methods(['POST','GET'])
def create_get_matzip(request):
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
                    status=200
                )

            new_matzip = Matzip.objects.create(
                name = body['name'],
                waiting = 0,
                matched = 0
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
                status=200
            )

    elif request.method == 'GET':
        matzip_all = Matzip.objects.all()

        matzip_name_list = []
        for matzip in matzip_all:
            matzip_name_list.append(matzip.name)
        
        json_res = json.dumps(
            {
                "success": True,
                "resList" : matzip_name_list
            },
            ensure_ascii=False
        )
            
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
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

        now_matzip_all = Matzip.objects.all().order_by('-matched')

        now_matzip_json_all = []
        for now_matzip in now_matzip_all:
            now_matching_all = Matching.objects.filter(matzip = now_matzip.id, is_closed = False,start_time__range=[datetime.now()+timedelta(seconds=1),datetime.now()+timedelta(days=30)]).order_by('start_time')
            
            # 맛집 대기팀 수(waiting) 갱신
            now_matzip.waiting = now_matching_all.count()
            now_matzip.save()

            if now_matzip.waiting == 0:
                now_matching_json_all=[]
                now_matching_json = {
                    "id" : 0
                }
                now_matching_json_all.append(now_matching_json)
                
            else:
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
                        "max" : now_matching.max_people+1,
                        "min" : now_matching.min_people+1, 
                        "id" : now_matching.id,
                        "description" : now_matching.bio,
                        "leader" : now_matching.leader.nickname, 
                        "follower": now_follower_json_all,
                        #"is_matched": now_matching.is_matched,
                        #"is_closed": now_matching.is_closed
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