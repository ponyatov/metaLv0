#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
from django.contrib import admin
from .models import *
# / <section:top>
# \ <section:mid>
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        'username',
        'loc',
        'last_name','first_name','father_name',
        'email','phone',
        'is_active','is_superuser'
        )

    fieldsets = (
        (None,{'fields':('username','password')}),
        (None,{'fields':('loc',)}),
        (None,{'classes': ('wide',),'fields':('last_name','first_name','father_name')}),
        (None,{'fields':('email','phone')}),
        (None,{'fields':('is_staff', 'is_active')}),
        )
    
admin.site.register(CustomUser,CustomUserAdmin)
# / <section:mid>
# \ <section:bot>
from django.contrib.gis.admin.options import OSMGeoAdmin

class CustomGeoAdmin(OSMGeoAdmin):
    default_lon = 5592262; default_lat = 7028511
    default_zoom = 6
    list_display = ['name', 'okato', 'kladr', 'pk', 'userbind']

admin.site.register(Location, CustomGeoAdmin)
# / <section:bot>
