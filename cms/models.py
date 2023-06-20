import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from product.models import Products
# Create your models here.


class Website_Setting(models.Model):
    """ Model class for Website_Setting """
    title = models.CharField(max_length=225)
    logo = models.ImageField(upload_to='logo')
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    address = models.TextField()

    def __str__(self):
        return self.title


class Slider(models.Model):
    """ model class for Slider """
    heading = models.CharField(max_length=255)
    sub_heading = models.CharField(max_length=255)
    image = models.ImageField(upload_to='slider')
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.heading}{self.sub_heading}"


class Blog(models.Model):
    """ model class for Blog """
    title = models.CharField(max_length=225)
    slug = models.SlugField()
    description = models.TextField()
    author = models.CharField(max_length=225)
    date_time = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog')
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}{self.author}"
    
    """ for slug setting """
    def save(self,*args,**kwargs):  
        self.slug= slugify(self.title)  
        super(Blog,self).save(*args, **kwargs) 

    
class FAQ(models.Model):
    """ model class for FAQ """
    question = models.CharField(max_length=225)
    answer = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name= 'FAQ'
        verbose_name_plural= 'FAQs'


