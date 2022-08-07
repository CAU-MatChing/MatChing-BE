from django.urls import path
from .views import *

urlpatterns = [ 
    path('', create_getall_matzip, name='create_getall_matzip'),
    path('now', getall_now_matzip, name='getall_now_matzip'),
    path('delete-matzip/<int:id>', delete_matzip, name='delete-matzip'),
    path('update-matzip/<int:id>', update_matzip, name='update-matzip'),
    path('get-matzip/<int:id>', get_matzip, name='get-matzip'),
]
