from django.contrib import admin
from user_profile.models import User_Profile
# Register your models here.

class addUser_Profile(admin.ModelAdmin):
    """ Register addUser_Profile to admin"""
    list_display=['id','user','mobile']
    list_filter=['user__first_name','user__last_name']
    search_fields=['user__first_name']

admin.site.register(User_Profile,addUser_Profile)
