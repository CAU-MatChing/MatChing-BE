from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from .models import Matching, Follower
from profiles.models import Profile
from matzips.models import Matzip
from datetime import datetime, timedelta
import json

@require_http_methods(['GET'])
def get_main(request):
    if request.method == 'GET':
        return JsonResponse({'success':True},status=200)
        
@require_http_methods(['POST'])
def create_matching(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            body = json.loads(request.body.decode('utf-8'))
            cur_matzip = get_object_or_404(Matzip,name=body['name'])
            
            #시작시간+지속시간 = 종료시간
            start = datetime.strptime(body['startTime'], "%Y-%m-%d %H:%M")
            time_str = body['duration']
            time_str = time_str.replace(" ", "")
            time_str = time_str.rstrip('분')
            list = time_str.split('시간')
            sum = int(list[0])*60 + int(list[1])
            end = start + timedelta(minutes=+sum)
            
            #이부분만 민경이랑 합의하면 됨
            new_matching = Matching.objects.create(
                leader = request.user.profile,
                matzip = cur_matzip,
                bio = body['description'],
                social_mode = body['mode'],
                desired_gender = body['gender'],
                desired_major = body['major'],
                min_people = body['min']-1,
                max_people = body['max']-1,
                start_time = start,
                end_time = end,
                duration = body['duration']
            )
            
            cur_matzip.waiting+=1
            cur_matzip.save()

            
            return JsonResponse({"success":True}, status=200)

        else:
            json_res = json.dumps(
                {
                    "success": False,
                    "errorMessage": "로그인이 필요합니다."
                },
                ensure_ascii=False
            )
                
            return HttpResponse(
                json_res,
                content_type=u"application/json; charset=utf-8",
                status=200
            )
        

#민경이가 안쓸듯?
@require_http_methods(['GET','DELETE'])
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
            "duration" : get_matching.duration,
			"followers": follower_json_all 
        }
            
        return HttpResponse(
            json.dumps(get_matching_json, ensure_ascii=False),
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
                "success": True
            },
            ensure_ascii=False
        )
            
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

# 팔로워가 매칭을 신청하는 코드
# 민경이랑 senddata/url 합의해야 함
@require_http_methods(['POST'])
def join_matching(request, matching_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # body = json.loads(request.body.decode('utf-8'))
            cur_matching = get_object_or_404(Matching, pk=matching_id)

            cur_user_profile = request.user.profile
            
            # 리더가 자신이 생성한 매칭을 신청한 경우 검사
            if cur_matching.leader == cur_user_profile:
                json_res = json.dumps(
                        {
                            "success": False,
                            "errorMessage": "본인이 생성한 맛칭은 신청할 수 없습니다."
                        },
                        ensure_ascii=False
                    )

                return HttpResponse(
                    json_res,
                    content_type=u"application/json; charset=utf-8",
                    status=200
                )

            # 이미 신청한 매칭을 중복 신청한 경우 검사
            if Follower.objects.filter(matching = cur_matching,profile=cur_user_profile).exists():
                json_res = json.dumps(
                        {
                            "success": False,
                            "errorMessage": "이미 신청한 맛칭입니다."
                        },
                        ensure_ascii=False
                    )

                return HttpResponse(
                    json_res,
                    content_type=u"application/json; charset=utf-8",
                    status=200
                )

            # 리더가 설정한 성별 조건에 맞는지 검사
            if(cur_matching.desired_gender == 'F' or cur_matching.desired_gender == 'M'):
                if(cur_matching.desired_gender != cur_user_profile.gender):
                    json_res = json.dumps(
                        {
                            "success": False,
                            "errorMessage": "성별 조건이 일치하지 않습니다."
                        },
                        ensure_ascii=False
                    )

                    return HttpResponse(
                        json_res,
                        content_type=u"application/json; charset=utf-8",
                        status=200
                    )
            
            # 리더가 설정한 전공 조건에 맞는지 검사
            if(cur_matching.desired_major != '학과 무관'):
                if(cur_matching.desired_major != cur_user_profile.major):
                    json_res = json.dumps(
                        {
                            "success": False,
                            "errorMessage": "전공 조건이 일치하지 않습니다."
                        },
                        ensure_ascii=False
                    )

                    return HttpResponse(
                        json_res,
                        content_type=u"application/json; charset=utf-8",
                        status=200
                    )
        
        
            new_follower = Follower.objects.create(
                matching = cur_matching,
                profile = request.user.profile,
            )


            follower_all = Follower.objects.filter(matching = cur_matching)

            if cur_matching.min_people <= len(follower_all):
                cur_matching.is_matched = True
                cur_matching.matzip.matched+=1
                cur_matching.matzip.save()
            else:
                cur_matching.is_matched = False
                
            if cur_matching.max_people <= len(follower_all):
                cur_matching.is_closed = True
            else:
                cur_matching.is_closed = False
            
            cur_matching.save()

            return JsonResponse({"success":True}, status=200)


        else:
            json_res = json.dumps(
                {
                    "success": False,
                    "errorMessage": "로그인이 필요합니다."
                },
                ensure_ascii=False
            )
                
            return HttpResponse(
                json_res,
                content_type=u"application/json; charset=utf-8",
                status=200
            )

            
# 팔로워가 매칭을 취소하는 코드 - 수정본(위에꺼는 수정전), url 추가는 안하고 함수만 새로 작성
@require_http_methods(['DELETE'])
def cancel_matching(request, matching_id):  
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            cur_matching = get_object_or_404(Matching, pk=matching_id)
            user_profile = request.user.profile
            
            #리더와 같은지 먼저 검사
            if cur_matching.leader == user_profile:
                #매칭 삭제되면 다른것도 다 알아서 삭제되겠지?
                cur_matching.delete()
                #맛집 웨이팅 빼주기
                cur_matzip = cur_matching.matzip
                cur_matzip.waiting -= 1
                cur_matzip.save()
            else:
                #팔로워 검사
                cur_follower = get_object_or_404(Follower, profile=user_profile, matching = cur_matching)
                cur_follower.delete()
                
                #팔로워 취소로 인한 매칭정보 갱신
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
                      
            return JsonResponse({"success":True}, status=200)

        else:
            json_res = json.dumps(
                {
                    "success": False,
                    "errorMessage": "로그인이 필요합니다."
                },
                ensure_ascii=False
            )
                
            return HttpResponse(
                json_res,
                content_type=u"application/json; charset=utf-8",
                status=200
            )