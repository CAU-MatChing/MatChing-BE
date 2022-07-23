from django.urls import path
from .views import *

urlpatterns = [ 
    path('create-matzip/', create_matzip, name='create-matzip'),
    path('delete-matzip/<int:id>', delete_matzip, name='delete-matzip'),
    path('update-matzip/<int:id>', update_matzip, name='update-matzip'),
    path('get-matzip/<int:id>', get_matzip, name='get-matzip'),
    path('get-all-matzip/', get_all_matzip, name='get-all-matzip'),
]
