from django.urls import path
from .views import *

urlpatterns = [ 
    path('<int:matzip_id>/new/', create_matching, name='create-matching'),
    path('<int:matching_id>/', read_update_delete_matching, name='read_update_delete_matching'),
    path('<int:matching_id>/follower/', join_cancel_matching, name='join_cancel_matching')
]
