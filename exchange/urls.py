from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-trader/', admin.site.urls),
    path('', include('trading.urls')),
]
