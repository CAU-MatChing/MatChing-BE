from django.urls import path
from .views import *

urlpatterns = [ 
    path('', create_get_matzip, name='create_get_matzip'),
    path('now/', getall_now_matzip, name='getall_now_matzip'),
    path('<int:id>/', get_delete_matzip, name='get_update_delete_matzip'),
]
