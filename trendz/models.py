
from typing_extensions import Required
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass


class Data(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="userd" )
    fs = models.IntegerField(null=True, blank=True, default=None)
    pp = models.IntegerField(null=True, blank=True, default=None)
    hba1c = models.FloatField(null=True, blank=True,default=None)
    hb = models.FloatField(null=True, blank=True, default=None)
    rbc = models.FloatField(null=True, blank=True, default=None)
    wbc = models.IntegerField(null=True, blank=True, default=None)
    pl = models.IntegerField(null=True, blank=True, default=None)
    cr = models.FloatField(null=True, blank=True,default=None)
    date = models.DateField(null=True )

    def serialize(self):
        return{
            "id": self.id,
            "user": self.user.username,
            "fs": self.fs,
            "pp": self.pp,
            "hba1c": self.hba1c,
            "hb": self.hb,
            "rbc": self.rbc,
            "wbc": self.wbc,
            "pl": self.pl,
            "cr": self.cr,
            "date": self.date,
        }



class Param(models.Model):
    param = models.CharField(max_length=20,null=True, blank=True, default=None )
    title = models.CharField(max_length=50, null=True, blank=True, default=None)
    normalval_low = models.FloatField(null=True, blank=True, default=None)
    normalval_high = models.FloatField(null=True, blank=True, default=None)

    def serialize(self):
        return{
            "param": self.param,
            "title": self.title,
            "normalval_low": self.normalval_low,
            "normalval_high": self.normalval_high,
        }