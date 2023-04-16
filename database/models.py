from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.related import ForeignKey, OneToOneField

from datetime import datetime

class User(AbstractUser):
    id_cards = models.CharField(null=False,blank=False,max_length=13)
    numbers = models.CharField(null=False,blank=False,max_length=10)

class FaceData(models.Model):
    user = OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(null=True)

    class Meta:
        ordering = ['user']
    def __str__(self):
        return str(self.user.id_cards)

class Quarantine(models.Model):
    user = OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(null=False,blank=False,max_length=20)
    lat = models.FloatField(null=False,blank=False)
    long = models.FloatField(null=False,blank=False)
    radius = models.FloatField(null=False,blank=False, default=50)
    address = models.TextField()
    STATUS_CHOICES = (
        ("verified","verified"),
        ("unverified","unverified"),
        ("inactive","inactive"),
        # ("passive")
    )
    quarantine_status = models.CharField(null=False,blank=False,max_length=10, choices=STATUS_CHOICES,default="verified")
    is_inside = models.BooleanField(null=False,default=True)
    start_date = models.DateTimeField(null=False,blank=False)
    last_checked = models.DateTimeField(null=True,blank=True)
    
    class Meta:
        ordering = ['user']
    def __str__(self):
        return str(self.user.id_cards)+" : "+str(self.name)+" - "+str(self.start_date)


class History(models.Model):
    quarantine = models.ForeignKey(Quarantine,on_delete=models.CASCADE)
    check_datetime = models.DateTimeField(null=True,blank=True)
    lat_check = models.FloatField(null=False,blank=False)
    long_check = models.FloatField(null=False,blank=False)

    def __str__(self):
        return str(self.quarantine.user.id_cards)+" : "+str(self.quarantine.name)+" : "+str(self.check_datetime)

class QuarantineDay(models.Model):
    days = models.FloatField(blank=True)

    def __str__(self):
        return str('Days : '+str(self.days))