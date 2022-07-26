from django.urls import path
from .views import *

urlpatterns = [ 
    path('create-matching/', create_matching, name='create-matching'),
    path('delete-matching/<int:id>', delete_matching, name='delete-matching'),
    path('update-matching/<int:id>', update_matching, name='update-matching'),
    path('get-matching/<int:id>', get_matching, name='get-matching'),
    path('get-all-matching/', get_all_matching, name='get-all-matching'),
]
