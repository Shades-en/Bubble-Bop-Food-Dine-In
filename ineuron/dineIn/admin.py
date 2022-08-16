from django.contrib import admin
from .models import FoodMenu, Table, User, Bill

# Register your models here.
admin.site.register(FoodMenu)
admin.site.register(Table)
admin.site.register(User)
admin.site.register(Bill)



