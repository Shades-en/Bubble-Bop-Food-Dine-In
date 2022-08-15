
from django.db import models
from django.contrib.postgres.fields import ArrayField
from jsonfield import JSONField

# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)


class FoodMenu(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=300)



class Table(models.Model):
    number = models.IntegerField(default=0)
    # capacity = models.IntegerField(default=5)
    status = models.BooleanField(default=False)
    totalPrice = models.IntegerField(default=0)
    order_payment_amount = models.IntegerField(default=0)
    order_payment_status = models.CharField(max_length=50)
    order_payment_id = models.CharField(max_length=50)
    order_no = models.CharField(max_length=50)
    # order_time = models.CharField(max_length=50)
    order_date = models.DateTimeField('date published')
    order_status = models.CharField(max_length=50)
    order = models.ForeignKey(FoodMenu, on_delete=models.DO_NOTHING)

# class Order(models.Model):
#     food = models.CharField(max_length=200)
#     quantity = models.IntegerField(default=0)
#     price = models.IntegerField(default=0)


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    tableNo = models.IntegerField(default=0)
    otp = models.IntegerField(default=0)
    orders = ArrayField(JSONField(), default=list)
