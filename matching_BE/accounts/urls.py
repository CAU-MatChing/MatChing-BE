# cy : add new file

from django.urls import path
from .views import *
   
urlpatterns = [
    path('signup/', SignUp.as_view(), name = 'signup'),
    path('activate/<str:uidb64>/<str:token>/', Activate.as_view(), name = 'activate'),
    path('login/',login, name = 'login'),
    path('logout/',logout, name = 'logout'),
    #path('withdraw/',views.Withdraw.as_view(), name = 'withdraw'),
]