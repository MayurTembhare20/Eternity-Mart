from django.contrib import admin,messages
from order.models import Order,Order_Details,Payment

# Register your models here.
class Order_Details_Inline(admin.TabularInline): 
    """ Register Order Details to admin """
    model = Order_Details


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
  
    
class add_order(admin.ModelAdmin):
    """ Register add_order to admin """
    list_display=['id','user','mobile','status','payment_status']
    list_filter=['user']
    search_fields=['user__first_name']
    inlines = (Order_Details_Inline,)
    actions = (active_status,inactive_status)

admin.site.register(Order,add_order)


class add_details(admin.ModelAdmin):
    """ Register add_details to admin """
    list_display=['id','order','product','price']
    list_filter=['price']
    search_fields=['id']

admin.site.register(Order_Details,add_details)


class add_payments(admin.ModelAdmin):
    """ Register add_payments to admin """
    list_display=['id','order','Payment_id','Payment_status','amount']
    list_filter=['Payment_id']
    search_fields=['id']

admin.site.register(Payment,add_payments)