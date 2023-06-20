from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save,post_delete,pre_delete


class User_Profile(models.Model):
    """ Model class for User_Profile"""
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='user_profile')
    mobile = models.CharField(max_length=12,blank=True, null=True)
    address = models.TextField(null=True) 

    def __str__(self):
        return f"{self.user.first_name}{self.user.last_name}"


@receiver(post_save, sender=User)
def create_profile(sender,instance,created, **kwargs):
    """ Operation """
    if created:
        User_Profile.objects.create(user=instance)