from django.db import models
from django.contrib.auth.models import User
from product.models import Products,Product_Variation
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save,post_delete,pre_delete

class Order(models.Model):
    """ Model class for Order """
    STATUS_CHOICE = (
        ('pending','pending'),
        ('Inprogress','Inprogress'),
        ('Dispatch','Dispatch'),
        ('Delivered','Delivered'),
        ('success','success'),
        ('Canceled','Canceled'),
        ('Rejected','Rejected'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    address = models.TextField()
    mobile = models.CharField(max_length=12)
    payment_status = models.BooleanField(default=False)
    status = models.CharField(max_length=50,choices=STATUS_CHOICE, default="Pending")
    razor_pay_order_id = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return str(self.id)
    

class Order_Details(models.Model):
    """ Model class for Order_Details """
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7,decimal_places=2)
    variation = models.ForeignKey(Product_Variation,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f"{self.order.id}{self.product.name}"
    
    class Meta:
        verbose_name= 'Order_Detail'
        verbose_name_plural= 'Order_Details'


class Payment(models.Model):
    """ Model class for Payment """
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    Payment_id = models.CharField(max_length=255,null=True)
    Payment_status = models.CharField(max_length=255,null=True)
    Payment_method = models.CharField(max_length=255 ,null=True)
    created_at = models.CharField(max_length=255, null=True) 
    amount = models.CharField(max_length=255, null=True) 
    
    def __str__(self):
        return str(self.Payment_id)
    
    class Meta:
        verbose_name= 'Payment_Detail'
        verbose_name_plural= 'Payment_Details'


@receiver(post_save, sender=User)
def create_profile(sender,instance,created, **kwargs):
    """ Connect to User to Order """
    if created:
        Order.objects.create(user=instance)