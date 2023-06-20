from django.db import models

class brand(models.Model):
    """ Model class for brand """
    name = models.CharField(max_length=225)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name