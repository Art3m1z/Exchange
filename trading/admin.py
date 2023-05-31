from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class AdminPanelUser(admin.ModelAdmin):
    search_fields = ['last_name', 'first_name', 'middle_name']


@admin.register(Assets)
class AdminPanelUser(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(Order)
class AdminPanelUser(admin.ModelAdmin):
    search_fields = ['user__last_name', 'user__first_name', 'user__middle_name', 'status', 'asset__title']

@admin.register(MarketData)
class AdminPanelUser(admin.ModelAdmin):
    search_fields = ['asset__title']


@admin.register(Subscription)
class AdminPanelUser(admin.ModelAdmin):
    search_fields = ['user__last_name', 'user__first_name', 'user__middle_name']