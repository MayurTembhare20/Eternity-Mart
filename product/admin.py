from django.contrib import admin,messages
from product.models import Product_Category,Product_Variation,Product_Tag,Products,Product_Image
# Register your models here

def active_status(modelAdmin, request, queryset):
    try:
        queryset.update(status= True)
        messages.success(request,'Selected record(s) marked as active')

    except Exception as e:
        messages.error(request, str(e))

  
def inactive_status(modelAdmin, request, queryset):
    try:
        queryset.update(status= False)
        messages.error(request,'Selected record(s) marked as inactive')

    except Exception as e:
        messages.error(request, str(e))
  

class Product_Images_Inline(admin.TabularInline): 
    """ Register Product_Images_Inline model to admin """
    model = Product_Image


class add_products(admin.ModelAdmin):
    """ Register addproducts model to admin """
    prepopulated_fields = {'slug':('name',)}
    list_display=['id','name','product_category','price','status']
    list_filter=['product_category']
    search_fields=['name']
    inlines = (Product_Images_Inline,)
    actions = (active_status,inactive_status)
    
admin.site.register(Products,add_products)

class add_category(admin.ModelAdmin):
    """ Register add_category model to admin """
    list_display=['id','name','slug','status', "show_on_homepage"]
    list_filter=['name']
    search_fields=['name']

admin.site.register(Product_Category,add_category)

class add_variation(admin.ModelAdmin):
    """ Register add_variation model to admin """
    list_display=['id','name','status']
    list_filter=['name']
    search_fields=['name']

admin.site.register(Product_Variation,add_variation)

class add_tags(admin.ModelAdmin):
    """ Register add_tags model to admin """
    list_display=['id','name','status']
    list_filter=['name']
    search_fields=['name']

admin.site.register(Product_Tag,add_tags)