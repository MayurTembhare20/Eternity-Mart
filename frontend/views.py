from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from Brand.models import brand
from cms.models import Slider,FAQ
from cms.models import Website_Setting,Blog
from product.models import Product_Category,Products,Product_Tag
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage


def home_page(request):
    """ Home page of website  """
    sliders = Slider.objects.filter(status=True)
    Product_category =  Product_Category.objects.filter(status=True, show_on_homepage=True)
    fashion_products_one =  Products.objects.select_related('product_category').filter(status= True)[0:2]
    fashion_products_two =  Products.objects.select_related('product_category').filter(status= True)[2:4]
    product_tags =  Product_Tag.objects.filter(status= True)[0:2]
    blogs = Blog.objects.filter(status= True)[0:2]
    context={
        'sliders': sliders,
        'Product_category': Product_category,
        'fashion_products_one' : fashion_products_one,
        'fashion_products_two' : fashion_products_two,
        'product_tags':product_tags,
        'blogs': blogs      
    }
    return render(request,'my_home.html',context)


def product_listing(request,product_category_slug=None):
        """ Products with category slug """
        search = request.GET.get('search')
        sorting = request.GET.get('sorting')
        filters = {
            'status':True
        }
        
        if search:
            filters['name__icontains'] = request.GET.get('search')
            products = Products.objects.select_related('product_category').filter(**filters)
        else:
            pass

        if product_category_slug:
            filters['product_category__slug'] = product_category_slug
            Products.objects.select_related('product_category').filter(**filters)
            
        if sorting == "low":
            products = (
                Products.objects.select_related('product_category').filter(**filters).order_by('price')
            )

        items_per_page = 3
        page  = request.GET.get('page',1)
        products = Products.objects.select_related('product_category').filter(**filters) # recomended
        paginator = Paginator(products, items_per_page)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(items_per_page)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
            
        if sorting == "high":
            products = (
                Products.objects.select_related('product_category').filter(**filters).order_by('-price')
            )
       
        context = {
            'products' : products,
            'page_obj' : products
        }
        return render(request,'product/product_listing.html',context)
    

class Product_Details(View):
    """ Product Details with product_slug """
    def get(self, request, product_slug):

        try:
            product = Products.objects.select_related('product_category').prefetch_related('Product_Image').get(slug=product_slug)
            similar_products = Products.objects.filter(status=True, product_category=product.product_category).exclude(id=product.id)
            context = {
                'product' : product,
                'similar_products' : similar_products,
            }
            return render(request, 'product/product_details.html', context)
        except Products.DoesNotExist:
            pass


def contact_page(request):
    """ create contact page """
    return render(request,'contact_us.html')


def about_page(request):
    """ create about page """
    brands= brand.objects.filter(status=True)
    return render(request,'about.html',{'brands': brands})


def faqs_page(request):
    """ create faqs page """
    faqs = FAQ.objects.filter(status= True)
    context={
        'faqs': faqs   
    }
    return render(request,'faqs.html',context)


def blog_details(request):
    """ create blog_details page """
    filters = {
        'status': True
        }
    if request.GET.get('find'):
        filters['slug__icontains'] = request.GET.get('find')

    blogs = Blog.objects.filter(**filters)
            
    context={
        'blogs': blogs
    }
    return render(request,'blog_details.html',context)

def single_post(request,blog_slug):
    """ create single_post page """
    filters = {
        'status': True
    }
    if request.GET.get('s'):
        filters['description__icontains'] = request.GET.get('s')

    if blog_slug:
        filters['slug'] = blog_slug
    blogs = Blog.objects.filter(**filters)
    
    context={
        'blogs': blogs       
    }
    return render(request,'blog_self_details.html',context)

def all_products(request):
    """ crete  all products page"""
    return render(request,'product/product_listing.html')
