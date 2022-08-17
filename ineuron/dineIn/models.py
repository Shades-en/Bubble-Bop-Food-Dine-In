from djongo import models
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
    number = models.IntegerField(default=1, primary_key=True)
    status = models.CharField(max_length=50)
    capacity = models.IntegerField(default=5)
    occupied_by = JSONField(null=True, blank=True)

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    tableNo = models.IntegerField(default=0)
    otp = models.IntegerField(default=0)
    otp_verified = models.BooleanField(default=False)

class Bill(models.Model):
    total = models.IntegerField(default=0)
    tax = models.FloatField(default=0)
    final_amt = models.FloatField(default=0)
    items = JSONField(null=True, blank=True)
    user = JSONField(null=True, blank=True)
    status = models.CharField(max_length=50, default="unpaid")
    time = models.DateTimeField(auto_now_add=True)


    
