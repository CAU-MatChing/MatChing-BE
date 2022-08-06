from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse,HttpResponse
from .models import *
import json

@require_http_methods(['POST','GET'])
def create_getall_matzip(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        
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
        return JsonResponse({
                'status': 405,
                'success': False,
                'message': 'Method Error',
                'data': None
            })
            
def delete_matzip(request, id):
    if request.method =="DELETE":
        delete_matzip = get_object_or_404(Matzip, pk=id)
        delete_matzip.delete()

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
        

        
def get_matzip(request, id):
    if request.method == "GET":
        get_matzip = get_object_or_404(Matzip, pk=id)
        
        get_matzip_json = {
            "name" : get_matzip.name,
            "location" : get_matzip.location,
            "waiting" : get_matzip.waiting
        }
        
        return JsonResponse({
            "data" : get_matzip_json
        })
    else:
        return JsonResponse({
                'status': 405,
                'success': False,
                'message': 'Get error',
                'data': None
            })
        
def update_matzip(request, id):
    if request.method == "PATCH":
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
        
        return JsonResponse({
            "data" : update_matzip_json
        })
    else:
        return JsonResponse({
                'status': 405,
                'success': False,
                'message': 'Get error',
                'data': None
            })
        
