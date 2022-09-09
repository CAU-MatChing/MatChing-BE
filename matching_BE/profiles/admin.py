from django.contrib import admin
from .models import Profile,Report

class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'account',
        'nickname', 
        'major', 
        'gender',
        'rudeness',
        'noshow',
        'cancel',
        'matching_num',
        'matching_people',
        'is_disabled',
        'release_date',
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
    list_filter = ('major','gender',)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('type', 'reporter', 'target', 'reason',)
    list_display_links = None
    list_editable = ('type', 'reporter', 'target',)
    list_filter = ('type','reporter','target',)

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Report,ReportAdmin)