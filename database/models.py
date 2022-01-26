from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.related import ForeignKey, OneToOneField

class User(AbstractUser):
    id_cards = models.CharField(null=False,blank=False,max_length=13)
    numbers = models.CharField(null=False,blank=False,max_length=10)

class FaceData(models.Model):
    user = OneToOneField(User,on_delete=models.CASCADE)
    data = models.TextField()

class Quarantine(models.Model):
    user = OneToOneField(User,on_delete=models.CASCADE)
    lat = models.FloatField(null=False,blank=False)
    long = models.FloatField(null=False,blank=False)
    detail = models.TextField()
    start_date = models.DateTimeField(null=False,blank=False)
    last_checked = models.DateTimeField(null=True,blank=True)