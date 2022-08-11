from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse,HttpResponse
from .models import *
from matchings.models import *
import json

@require_http_methods(['POST','GET'])
def create_getall_matzip(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            body = json.loads(request.body.decode('utf-8'))
            
            if Matzip.objects.filter(name = body['name']).exists():
                json_res = json.dumps(
                        {
                            "status": 400,
                            "success": False,
                            "message": "이미 존재하는 식당",
                            "data": None
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
                location = body['location'],
                waiting = 0
            )
            
            new_matzip_json = {
                "name" : new_matzip.name,
                "location" : new_matzip.location,
                "waiting" : new_matzip.waiting
            }

            json_res = json.dumps(
                {
                    "status": 200,
                    "success": True,
                    "message": "생성 성공",
                    "data": new_matzip_json
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

    elif request.method == 'GET':
        matzip_all = Matzip.objects.all()
        
        matzip_json_all = []
        for matzip in matzip_all:
            matzip_json = {
                "name" : matzip.name,
                "location" : matzip.location,
                "waiting" : matzip.waiting
            }
            matzip_json_all.append(matzip_json)
            
        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "맛집 모두 읽기 성공",
                "data": matzip_json_all
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


@require_http_methods(['DELETE','PATCH','GET'])  
def get_update_delete_matzip(request, id):
    if request.method == "GET":
        get_matzip = get_object_or_404(Matzip, pk=id)
        
        get_matzip_json = {
            "name" : get_matzip.name,
            "location" : get_matzip.location,
            "waiting" : get_matzip.waiting
        }
        
        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "맛집 단일 조회 성공",
                "data": get_matzip_json
            },
            ensure_ascii=False
        )
            
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

    elif request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        update_matzip = get_object_or_404(Matzip, pk=id)
        
        update_matzip.name = body['name']
        update_matzip.location = body['location']
        
        update_matzip.save()
        
        update_matzip_json = {
            "name" : update_matzip.name,
            "location" : update_matzip.location,
            "waiting" : update_matzip.waiting
        }
        
        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "맛집 수정 성공",
                "data": update_matzip_json
            },
            ensure_ascii=False
        )
            
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

    elif request.method =="DELETE":
        delete_matzip = get_object_or_404(Matzip, pk=id)
        delete_matzip.delete()

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "맛집 삭제 성공",
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
def getall_now_matzip(request):
    if request.method == "GET":
        now_matzip_all = Matzip.objects.all()

        now_matzip_json_all = []
        for now_matzip in now_matzip_all:
            now_matching_all = Matching.objects.filter(matzip = now_matzip.id, is_closed = False)
            
            now_matching_json_all=[]
            for now_matching in now_matching_all:
                now_follower_all = Follower.objects.filter(matching = now_matching.id)
                
                now_follower_json_all=[]
                for now_follower in now_follower_all:
                    now_follower_json_all.append(now_follower.profile.nickname)
                
                now_matching_json = {
                    "matching_id" : now_matching.id,
                    "matzip" : now_matching.matzip.name,
                    "bio" : now_matching.bio,
                    "leader" : now_matching.leader.nickname,
                    "created_time" : now_matching.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "remain" : now_matching.max_people-len(now_follower_json_all),
                    "is_matched" : now_matching.is_matched,
                    "is_closed" : now_matching.is_closed,
                    "social_mode" : now_matching.social_mode,
                    "desired_gender" : now_matching.desired_gender,
                    "desired_major" : now_matching.desired_major,
                    "min_people" : now_matching.min_people,
                    "max_people" : now_matching.max_people,
                    "start_time" : now_matching.start_time.strftime("%Y-%m-%d %H:%M"),
                    "end_time" : now_matching.end_time.strftime("%Y-%m-%d %H:%M"),
                    "duration" : now_matching.duration,
			        "followers": now_follower_json_all 
                }
                now_matching_json_all.append(now_matching_json)
                
            now_matzip_json = {
                "name" : now_matzip.name,
                "location" : now_matzip.location,
                "waiting" : now_matzip.waiting,
                "matchings" : now_matching_json_all
            }
            now_matzip_json_all.append(now_matzip_json)
        
        json_res = json.dumps(
                {
                    "status": 200,
                    "success": True,
                    "message": "맛집별 매칭 전체 조회 성공",
                    "data": now_matzip_json_all
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