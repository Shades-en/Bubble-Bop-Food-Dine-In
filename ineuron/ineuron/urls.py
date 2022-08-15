from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('dineIn/', include('dineIn.urls')),
    path('admin/', admin.site.urls),
]