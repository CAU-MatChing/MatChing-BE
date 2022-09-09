from django.contrib import admin
from .models import Matzip

class MatzipAdmin(admin.ModelAdmin):
    list_display = ('name', 'waiting', 'matched',)
    list_display_links = ('name',)
    # list_editable = ('name', 'matched',)
    list_filter = ('name','matched',)

admin.site.register(Matzip,MatzipAdmin)