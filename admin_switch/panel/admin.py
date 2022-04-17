from django.contrib import admin
from .models import *

admin.site.site_header = 'Moscow Switch Administration'


@admin.register(User)
class User_admin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'status']


@admin.register(Admin)
class Admin_list(admin.ModelAdmin):
    list_display = ['tg_id']


@admin.register(ADS_db)
class ADS_admin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'link', 'desc', 'address']


@admin.register(Who)
class Who_admin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Kategory)
class Kategory_admin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'for_who']
    list_filter = ('for_who', )


@admin.register(PlacesGroup)
class Group_admin(admin.ModelAdmin):
    list_display = ['name', 'kategory']
    list_filter = ('kategory', )


@admin.register(Place)
class User_admin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'group']
    list_filter = ('group', )


@admin.register(ActPlace)
class Act(admin.ModelAdmin):
    list_display = ['name', 'desc']

