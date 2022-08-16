
from queue import Empty
from django.db import models
from django.contrib.postgres.fields import ArrayField
from jsonfield import JSONField


class FoodMenu(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=300)

class Table(models.Model):
    number = models.IntegerField(default=0)
    status = models.CharField(max_length=50)
    capacity = models.IntegerField(default=5)
   

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    tableNo = models.IntegerField(default=0)
    otp = models.IntegerField(default=0)
    # orders = ArrayField(JSONField(), default=list)
