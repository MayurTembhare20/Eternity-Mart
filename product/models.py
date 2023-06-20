from django.db import models
from Brand.models import brand
from django.template.defaultfilters import slugify


class Product_Category(models.Model):
    """ Model class for Product_Category """
    name = models.CharField(max_length=225)
    slug = models.SlugField(max_length=225,null=True,blank=True)
    image = models.ImageField(upload_to='product_categories')
    status = models.BooleanField(default=True)
    show_on_homepage = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name= 'product_ category'
        verbose_name_plural= 'product_categories'
    
    # for slug setting
    def save(self,*args,**kwargs):
        self.slug= slugify(self.name)  
        super(Product_Category,self).save(*args, **kwargs)
    

class Product_Variation(models.Model):
    """ Model class for Product_Variation """
    name = models.CharField(max_length=225)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Product_Tag(models.Model):
    """ Model class for Product_Tag """
    name = models.CharField(max_length=225)
    slug = models.SlugField(max_length=225,null=True,blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    # for slug setting
    def save(self,*args,**kwargs):  
        self.slug= slugify(self.name) 
        super(Product_Tag,self).save(*args, **kwargs)


class Products(models.Model):
    """ Model class for Products """
    product_category = models.ForeignKey(Product_Category,on_delete=models.CASCADE,related_name='product_category')
    brand = models.ForeignKey(brand,on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=225)
    slug = models.SlugField(max_length=225,null=True,blank=True)
    cover_image = models.ImageField(upload_to='products')
    price = models.DecimalField(max_digits=7,decimal_places=2)
    description = models.TextField()
    variation = models.ManyToManyField(Product_Variation, blank=True)
    tags = models.ManyToManyField(Product_Tag, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name= 'product '
        verbose_name_plural= 'products'
        ordering = ['price']
    
    def save(self,*args,**kwargs):  
        self.slug= slugify(self.name)  
        super(Products,self).save(*args, **kwargs)
    

class Product_Image(models.Model):
    """ Model class for Product_Image """
    product= models.ForeignKey(Products,on_delete=models.CASCADE, related_name="Product_Image") # , related_name="ProductImage"==for showing similar product
    image = models.ImageField(upload_to='products')

    def __str__(self):
        return str(self.id)