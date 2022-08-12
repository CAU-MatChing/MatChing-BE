from .models    import *
from .tokens    import account_activation_token
from .text  import message
from profiles.models    import Profile
from matching_BE.settings   import *


EMAIL_USE_TLS = get_secret("EMAIL_USE_TLS")
EMAIL_PORT = get_secret("EMAIL_PORT")

import json
from django.views                    import View
from django.http                     import JsonResponse,HttpResponse
from django.core.exceptions          import ValidationError
from django.core.validators          import validate_email
from django.db                       import IntegrityError
from django.contrib.sites.shortcuts  import get_current_site
from django.shortcuts                import render, redirect
from django.utils.encoding           import force_bytes, force_str
from django.utils.http               import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth             import login as auth_login, logout as auth_logout,authenticate
from django.views.decorators.http    import require_http_methods
from datetime                        import date
import smtplib
from email.mime.text import MIMEText

# Create your views here.

def sign_up(request) :
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        try:
            # 이메일 유효성을 검사(메세지를 받을 수 있는 이메일인가?)
            validate_email(body["email"])
            email     = body["email"]
            password  = body["password"]
            
            # email에 @cau.ac.kr로 끝나지 않으면 에러메세지 반환하는 코드를 추가
            if "@cau.ac.kr" not in email:
                return JsonResponse({"message" : "BAD_EMAIL"}, status=400)
            
            # 디비에 저장
            user = Account.objects.create_user(email, password)
            
            # 이메일 보내기
            current_site = get_current_site(request) 
            domain       = current_site.domain
            uidb64       = urlsafe_base64_encode(force_bytes(user.pk))
            token        = account_activation_token.make_token(user)
            message_data = message(domain, uidb64, token)
            
            #메일발송설정
            sendEmail = EMAIL_HOST_USER
            recvEmail = body["email"]
            password = EMAIL_HOST_PASSWORD
            smtpName = EMAIL_HOST #smtp 서버 주소
            smtpPort = EMAIL_PORT #smtp 포트 번호
            
            msg = MIMEText(message_data)
            msg['Subject'] = "MatChing 서비스 회원가입을 위한 이메일 인증을 완료해주세요."
            msg['From'] = sendEmail
            msg['To'] = recvEmail
            
            s=smtplib.SMTP(smtpName , smtpPort) #메일 서버 연결
            s.starttls() #TLS 보안 처리
            s.login(sendEmail , password) #로그인
            s.sendmail(sendEmail, recvEmail, msg.as_string()) #메일 전송, 문자열로 변환하여 보냅니다.
            
            return JsonResponse({"message" : "SUCCESS"}, status=200)
       
        except IntegrityError:
            return JsonResponse({"message" : "Error"}, status=400)
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status=400)
        except TypeError:
            return JsonResponse({"message" : "INVALID_TYPE"}, status=400)
        except ValidationError:
            return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)
        
def activate(request, uidb64, token) :
    if request.method == 'GET':
        try:
            uid  = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
            
            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()

                return redirect('https://github.com/hectick') #리다이렉트 페이지
        
            return JsonResponse({"message" : "AUTH FAIL"}, status=400)

        except ValidationError:
            return JsonResponse({"message" : "TYPE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status=400)


def login(request) :
    if request.method == 'POST':
        body = json.loads(request.body.decode('UTF-8'))

        email = body['email']
        password = body['password']
        user = authenticate(request,email=email,password=password)

        if user is not None:
            auth_login(request,user)
            
            cur_user = request.user
            
            if cur_user.profile.is_disabled == True:
                if cur_user.profile.release_date > date.today():
                    auth_logout(request)
        
                    json_res = json.dumps(
                        {
                            "success": True,
                            "message": "정지 회원",
                        },
                        ensure_ascii=False
                    )
                    
                    return HttpResponse(
                        json_res,
                        content_type=u"application/json; charset=utf-8",
                        status=400
                    )
                
                else:
                    cur_user.profile.is_disabled = False
                    cur_user.profile.save()

            json_res = json.dumps(
                {
                    "success": True,
                    "message": "로그인 성공",
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
                    "success": False,
                    "message": "로그인 실패",
                },
                ensure_ascii=False
            )
                
            return HttpResponse(
                json_res,
                content_type=u"application/json; charset=utf-8",
                status=400
            )

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        
        json_res = json.dumps(
            {
                "success": True,
                "message": "로그아웃 성공",
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
                "success": False,
                "message": "사용자인증실패",
            },
            ensure_ascii=False
        )
            
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=401
        )

@require_http_methods(['POST'])
def delete_account(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
        
        json_res = json.dumps(
                {
                    "success": True,
                    "message": "회원탈퇴성공",
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
                "success": False,
                "message": "사용자인증 없음",
            },
        )
            
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=401
        )