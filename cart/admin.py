from django.contrib import admin
from cart.models import Cart

# Register your models here.

class adam(admin.ModelAdmin):
    """ Register adam to admin """
    list_display=['id','user','product','variation','quantity']
    list_filter=['user','product']
    search_fields=['user__first_name']

admin.site.register(Cart,adam)