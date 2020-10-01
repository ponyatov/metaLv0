#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
# / <section:top>
# \ <section:mid>
	path('', views.index, name='index'),
	path('admin/', admin.site.urls, name='admin'),
# / <section:mid>
# \ <section:bot>
]
# / <section:bot>
