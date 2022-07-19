from django.shortcuts import render

# cy : import
from .models    import Account
from .tokens    import account_activation_token
from .text  import message
from matching_BE.settings   import *


EMAIL_USE_TLS = get_secret("EMAIL_USE_TLS")
EMAIL_PORT = get_secret("EMAIL_PORT")

import json
from django.views                    import View
from django.http                     import JsonResponse
from django.core.exceptions          import ValidationError
from django.core.validators          import validate_email
from django.contrib.sites.shortcuts  import get_current_site
from django.shortcuts                import redirect
from django.utils.encoding           import force_bytes, force_str
from django.utils.http               import urlsafe_base64_encode,urlsafe_base64_decode

import smtplib
from email.mime.text import MIMEText

# Create your views here.

class SignUp(View):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        try:
            # 이메일 유효성을 검사(메세지를 받을 수 있는 이메일인가?)
            validate_email(body["email"])
            
            # email에 @cau.ac.kr로 끝나지 않으면 에러메세지 반환하는 코드를 추가
            
            user = Account.objects.create(
                email     = body["email"],
                password  = body["password"],
                is_active = False 
            )
            
            # 메세지 내용 추가
            #message_data = "메일 보내기 연습 본문입니다."
            
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
       
       
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status=400)
        except TypeError:
            return JsonResponse({"message" : "INVALID_TYPE"}, status=400)
        except ValidationError:
            return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)
        
class Activate(View):
    def get(self, request, uidb64, token):
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