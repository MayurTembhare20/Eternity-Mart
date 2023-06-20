from django.urls import path,include
from .views import (home_page,
                    product_listing,
                    contact_page,
                    Product_Details,
                    blog_details,
                    about_page,
                    faqs_page,
                    all_products,
                    single_post
                    )

urlpatterns = [      
    path('',home_page,name='home_page'),    
    path('product-listing/', product_listing, name="product_listing"),
    path('product_listing/<slug:product_category_slug>',product_listing,name='product_listing'),  
    path('product_details/<slug:product_slug>',Product_Details.as_view(),name='Product_Details'),  
    path('contact_us/',contact_page,name='contact_page'), 
    path('about/',about_page,name='about_page'), 
    path('faqs/',faqs_page,name='faqs_page'), 
    path('blog_details/',blog_details,name='blog_details'), 
    path('blog_details/single_post/<slug:blog_slug>',single_post,name='single_post'), 
    path('product_listing/<slug:product_category_slug>',all_products,name='all_products'),  
]