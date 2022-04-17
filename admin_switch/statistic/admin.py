from django.contrib import admin
from .models import *


@admin.register(UserStat)
class UserStatView(admin.ModelAdmin):
    list_display = ['tg_id', 'name', 'phone', 'visit_now', 'visit_future']
    sortable_by = 'visit_future'


@admin.register(IventStatistic)
class IventStatisticsView(admin.ModelAdmin):
    list_display = ['place', 'visit_now', 'visit_future']
    sortable_by = 'visit_future'

