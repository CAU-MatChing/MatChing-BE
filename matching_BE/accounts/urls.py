# cy : add new file

from django.urls import path
from .views import *
   
urlpatterns = [
    path('signup/', sign_up, name = 'sign_up'),
    path('activate/<str:uidb64>/<str:token>/', activate, name = 'activate'),
    path('login/',login, name = 'login'),
    path('logout/',logout, name = 'logout'),
    path('delete/',delete_account, name = 'delete_account'),
    path('login_check/',check_login, name = 'check_login'),
]