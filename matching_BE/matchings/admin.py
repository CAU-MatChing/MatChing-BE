from django.contrib import admin
from .models import Matching,Follower

class MatchingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'leader', 
        'matzip', 
        'is_matched',
        'is_closed',
        'social_mode',
        'desired_gender',
        'desired_major',
        'min_people',
        'max_people',
        'start_time',
        'end_time',
        'duration'
    )
    list_display_links = list_display
    # list_editable = (
    #     'leader', 
    #     'matzip', 
    #     'is_matched',
    #     'is_closed',
    #     'social_mode',
    #     'desired_gender',
    #     'desired_major',
    #     'min_people',
    #     'max_people',
    #     'start_time',
    #     'end_time',
    #     'duration',
    # )
    list_filter = ('leader','matzip','is_matched','is_closed','social_mode','desired_gender','desired_major',)

class FollowerAdmin(admin.ModelAdmin):
    list_display = ('matching', 'profile',)
    list_display_links = ('matching','profile',)
    list_filter = ('matching','profile',)

admin.site.register(Matching,MatchingAdmin)
admin.site.register(Follower,FollowerAdmin)