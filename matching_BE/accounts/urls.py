# cy : add new file

from django.urls import path
from . import views
   
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name = 'signup'),
    path('activate/<str:uidb64>/<str:token>/', views.Activate.as_view(), name = 'activate'),
    #path('login/',views.LogIn.as_view(), name = 'login'),
    #path('logOut/',views.LogOut.as_view(), name = 'logout'),
    #path('withdraw/',views.Withdraw.as_view(), name = 'withdraw'),
]