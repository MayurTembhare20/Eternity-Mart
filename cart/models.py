from django.db import models
from django.contrib.auth.models import User
from product.models import Product_Variation, Products


class Cart(models.Model):
    """ Model class for Cart """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    variation = models.ForeignKey(Product_Variation,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product}"



