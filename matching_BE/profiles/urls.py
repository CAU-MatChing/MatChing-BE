from django.urls import path
from .views import *

urlpatterns = [ 
    path('create-profile/', create_profile, name='create-profile'),
    path('delete-profile/<int:id>', delete_profile, name='delete-profile'),
]

