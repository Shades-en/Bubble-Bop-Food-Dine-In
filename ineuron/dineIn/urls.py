from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>', views.index, name='index'),
    path('<int:id>/delete', views.delete, name='delete'),
    path('<int:id>?otp=<int:otp>?verify=<str:user_id>/food_menu', views.food_menu, name='food_menu'),
]