from django.urls import path
from .views import *

urlpatterns = [ 
    path('', create_getall_matzip, name='create_getall_matzip'),
    path('now/', getall_now_matzip, name='getall_now_matzip'),
    path('<int:id>/', get_update_delete_matzip, name='get_update_delete_matzip'),
]
