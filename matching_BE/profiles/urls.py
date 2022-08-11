from django.urls import path
from .views import *

urlpatterns = [ 
    path('', create_profile, name='create-profile'),
    path('<int:id>', delete_profile, name='delete-profile'),
    path('my-matchings', get_my_matchings, name='get-my-matchings'),
]

