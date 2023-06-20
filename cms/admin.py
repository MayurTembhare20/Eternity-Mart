from django.contrib import admin,messages
from cms.models import Website_Setting,Slider,Blog,FAQ

# Register your models here.
def active_status(modelAdmin, request, queryset):
    """ Register active_status to admin """
    try:
        queryset.update(status= True)
        messages.success(request,'Selected record(s) marked as active')

    except Exception as e:
        messages.error(request, str(e))

  
def inactive_status(modelAdmin, request, queryset):
    """ Register inactive_status to admin """
    try:
        queryset.update(status= False)
        messages.error(request,'Selected record(s) marked as inactive')

    except Exception as e:
        messages.error(request, str(e))

class add_website(admin.ModelAdmin):
    """ Register add_website to admin """
    list_display=['id','title','logo','email','phone']
    list_filter=['title']
    search_fields=['title']

admin.site.register(Website_Setting,add_website)


class add_slider(admin.ModelAdmin):
    """ Register add_slider to admin """
    list_display=['id','heading','sub_heading','status']
    list_filter=['heading']
    search_fields=['heading']
    actions = (active_status,inactive_status)

admin.site.register(Slider,add_slider)


class add_blog(admin.ModelAdmin):
    """ Register add_blog to admin """
    prepopulated_fields = {'slug':('title',)}
    list_display=['id','title','author','status']
    list_filter=['title']
    search_fields=['title']
    actions = (active_status,inactive_status)

admin.site.register(Blog,add_blog)


class add_faq(admin.ModelAdmin):
    """ Register add_faq to admin """
    list_display=['id','question','answer','status']
    list_filter=['question']
    search_fields=['question']
    actions = (active_status,inactive_status)

admin.site.register(FAQ,add_faq)
