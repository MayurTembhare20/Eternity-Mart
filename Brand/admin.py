from django.contrib import admin,messages
from Brand.models import brand

# Register your models here.
def active_status(modelAdmin, request, queryset):
    """ Register active status to admin """
    # messages.success = show green alert
    # messages.error = show red alert
    # messages.warning = show brown alert
    # messages.info = show green alert
    try:
        queryset.update(status= True)
        messages.success(request,'Selected record(s) marked as active')

    except Exception as e:
        messages.error(request, str(e))

  
def inactive_status(modelAdmin, request, queryset):
    """ Register inactive status to admin """
    try:
        queryset.update(status= False)
        messages.error(request,'Selected record(s) marked as inactive')

    except Exception as e:
        messages.error(request, str(e))
  

class add_brand(admin.ModelAdmin):
    """ Register add_brand status to admin """
    list_display = ('id','name','status')
    list_filter = ['status']
    search_fields = ['name']
    actions = (active_status,inactive_status)

admin.site.register(brand,add_brand)